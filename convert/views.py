from django.shortcuts import render_to_response
from django.shortcuts import HttpResponse
from django.views.static import serve
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from convert.models import Music
from django.shortcuts import render
import wave 
import struct 
import numpy 
import operator 
from mingus.containers.Note import Note 
from numpy.fft import fft 
import os
import wave
import struct
import numpy
from mingus.containers.Note import Note
from numpy.fft import fft as _fft
import operator
import time
from django.core.servers.basehttp import FileWrapper
###########################note to midi############################################ 

from mingus.containers.Note import Note
from midiutil.MidiFile import MIDIFile
from mingus.midi import MidiFileOut
from mingus.containers.NoteContainer import NoteContainer


# Create the MIDIFile Object






#####################################################################

# Making a frequency-amplitude table 
# The log function turns out to be really, really slow, which adds up quickly. 
# So before we do any performance critical calculations we set up a cache of 
# all the frequencies we need to look up. 
_log_cache = []
for x in xrange(129):
    _log_cache.append(Note().from_int(x).to_hertz())

_last_asked = None

def _find_log_index(f):
    global _last_asked, _log_cache
    begin, end = 0, 128

    # Most calls are sequential, this keeps track of the last value asked for
    # so that we need to search much, much less. 
    if _last_asked is not None:
        lastn, lastval = _last_asked
        if f >= lastval:
           if f <= _log_cache[lastn]:
               _last_asked = lastn, f
               return lastn
           elif f <= _log_cache[lastn + 1]:
               _last_asked = lastn + 1, f
               return lastn + 1
           begin = lastn
    
    # Do some range checking
    if f > _log_cache[127] or f <= 0:
        return 128

    # Binary search related algorithm to find the index
    while begin != end:
        n = (begin + end) / 2 
        c = _log_cache[n]
        cp = _log_cache[n - 1] if n != 0 else 0
        if cp < f <= c:
            _last_asked = n, f
            return n 

        if f < c:
            end = n
        else:
            begin = n
    _last_asked = begin, f
    return begin


def find_frequencies(data, freq = 44100, bits = 16):
    # Fast fourier transform
    n = len(data)
    p = _fft(data)
    uniquePts = numpy.ceil((n + 1) / 2.0)

    # Scale by the length (n) and square the value to get the amplitude
    p = [ (abs(x) / float(n)) ** 2 * 2 for x in p[0:uniquePts] ]
    p[0] = p[0] / 2
    if n % 2 == 0:
        p[-1] = p[-1] / 2

    # Generate the frequencies and zip with the amplitudes
    s = freq / float(n)
    freqArray = numpy.arange(0, uniquePts * s, s)
    return zip(freqArray, p)


def find_notes(freqTable, maxNote = 100):
    res = [0] * 129
    n = Note()
    for freq, ampl in freqTable:
        if freq > 0 and ampl > 0:
            f = _find_log_index(freq)
            if f < maxNote:
                res[f] += ampl
            else:
                res[128] += ampl

    return [ (Note().from_int(x) if x < 128 else None, n) for x, n in enumerate(res) ]

def data_from_file(file):
    fp = wave.open(file, "r")
    data = fp.readframes(fp.getnframes())
    channels = fp.getnchannels()
    freq = fp.getframerate()
    bits = fp.getsampwidth()

    # Unpack bytes -- 
    #warning currently only tested with 16 bit wavefiles. 32 bit not supported. 
    data = struct.unpack("%sh" % fp.getnframes() * channels, data)

    # Only use first channel
    channel1 = []
    n = 0
    for d in data:
        if n % channels == 0:
                channel1.append(d)
        n += 1

    fp.close()
    return (channel1, freq, bits)

def find_Note(data, freq, bits):
    data = find_frequencies(data, freq, bits)
    return sorted(find_notes(data), key = operator.itemgetter(1))[-1][0]


def analyze_chunks(data, freq, bits, chunksize = 512):
    res = []
    while data != []:
        f = find_frequencies(data[:chunksize], freq, bits)
        res.append(sorted(find_notes(f), key = operator.itemgetter(1))[-1][0])
        data = data[chunksize:]
    return res


def find_melody(file, chunksize):
   	data, freq, bits = data_from_file(file)
	res = []
	for d in analyze_chunks(data, freq, bits, chunksize):
		if res != []:
           		if res[-1][0] == d:
           				val = res[-1][1]
           				res[-1] = (d, val + 1)
           		else:
        		    res.append((d, 1))
		else:
    			res.append((d, 1))
	return [ (x, freq) for x,freq in res]



#print is_most_likely("test.wav")

def uploader(request):
	if request.method == 'POST':
		wavnew = Music(wavfile = request.FILES['wavfile'])	
		wavfile1 = request.FILES['wavfile']	
		results= find_melody(file = wavfile1, chunksize = 512)	
		nc = results
		MyMIDI = MIDIFile(1)

# Add track name and tempo. The first argument to addTrackName and
# addTempo is the time to write the event.
		track = 0
		time = 0
		tempo=120
		MyMIDI.addTrackName(track,time,"Sample Track")
		MyMIDI.addTempo(track,time, tempo)

		i=0;
		n=len(nc)

		while i<n:
			channel = 0
			pitch = int(Note(nc[i][0]))
			duration = nc[i][1]
			i=i+1
			volume = 100
			time=time+duration
			MyMIDI.addNote(track,channel,pitch,time,duration,volume)


# And write it to disk.
		binfile = open("output.mid", 'wb')
		MyMIDI.writeFile(binfile)
		binfile.close()		
		wavnew.save()
		#filepath = "output.mid"
		##return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
		return render_to_response('convert/results.html', {'results':results}, RequestContext(request))		
		#return HttpResponseRedirect(reverse('convert.views.uploader'))
			
	else:
		return render_to_response('convert/index.html', {}, RequestContext(request))

def dloadmidi(request):
	filename = "output.mid"
	wrapper = FileWrapper(file(filename))
	response = HttpResponse(wrapper, content_type='text/plain')
	response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(filename)
	response['Content-Length'] = os.path.getsize(filename)
	return response

def dloadpdf(request):
	os.system("midi2ly output.mid")
	time.sleep(1)
	os.system("lilypond output-midi.ly")
	filename = "output-midi.pdf"
	wrapper = FileWrapper(file(filename))
	response = HttpResponse(wrapper, content_type='text/plain')
	response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(filename)
	response['Content-Length'] = os.path.getsize(filename)
	return response

