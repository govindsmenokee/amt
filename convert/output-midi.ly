% Lily was here -- automatically converted by /usr/bin/midi2ly from output.mid
\version "2.14.0"

\layout {
  \context {
    \Voice
    \remove "Note_heads_engraver"
    \consists "Completion_heads_engraver"
    \remove "Rest_engraver"
    \consists "Completion_rest_engraver"
  }
}

trackAchannelA = {


  \key c \major
    
  \time 4/4 
  

  \key c \major
  
}

trackA = <<
  \context Voice = voiceA \trackAchannelA
>>


trackBchannelB = \relative c {
  \voiceOne
  e'4*231/220 r4*25/220 d4*231/220 r4*25/220 c4*231/220 r4*25/220 d4*231/220 
  r4*25/220 e4*231/220 r4*25/220 e4*231/220 r4*25/220 e4*462/220 
  r4*50/220 d4*231/220 r4*25/220 d4*231/220 r4*25/220 d4*462/220 
  r4*50/220 e4*231/220 r4*25/220 g4*231/220 r4*25/220 g4*462/220 
  r4*50/220 e4*231/220 r4*25/220 d4*231/220 r4*25/220 c4*231/220 
  r4*25/220 d4*231/220 r4*25/220 e4*231/220 r4*25/220 e4*231/220 
  r4*25/220 e4*231/220 r4*25/220 e4*231/220 r4*25/220 d4*231/220 
  r4*25/220 d4*231/220 r4*25/220 e4*231/220 r4*25/220 d4*231/220 
  r4*25/220 <c e, >4*974/220 
}

trackBchannelBvoiceB = \relative c {
  \voiceTwo
  g' r4*50/220 g4*974/220 r4*50/220 g4*974/220 r4*50/220 g4*974/220 
  r4*50/220 g4*974/220 r4*50/220 g4*974/220 r4*50/220 g4*974/220 
}

trackB = <<
  \context Voice = voiceA \trackBchannelB
  \context Voice = voiceB \trackBchannelBvoiceB
>>


\score {
  <<
    \context Staff=trackB \trackA
    \context Staff=trackB \trackB
  >>
  \layout {}
  \midi {}
}
