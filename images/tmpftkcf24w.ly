\version "2.7.40"
\header {
	composer = "Tommy Potts"
	footnotes = ""
	tagline = "Lily was here 2.18.2 -- automatically converted from ABC"
	title = "The Butterfly"
}
voicedefault =  {
\set Score.defaultBarType = ""

\repeat volta 2 {
\time 9/8 \key e \minor   b'4 ^\downbow   e'8 (   g'4  -)   e'8 (   fis'4.  -) 
\bar "|"   b'4    e'8 (   g'4  -)   e'8 (   fis'8  -)   e'8    d'8  \bar "|"   
b'4 ^\downbow   e'8 (   g'4  -)   e'8 (   fis'4.  -) \bar "|"   b'4 (   d''8  
-)   d''4      b'8 (^\upbow   a'8  -)   fis'8    d'8  }     \repeat volta 2 {   
  b'4 (^\downbow   c''8  -)   e''4 (   fis''8  -)   g''4.  \bar "|"     b'4 
(^\upbow   d''8  -)   g''4 (   e''8  -)   d''8 (   b'8    a'8  -) \bar "|"   
b'4 (   c''8  -)   e''4 (   fis''8  -)   g''4      a''8 (^\upbow \bar "|"   
b''4    a''8  -)   g''4 (   e''8  -)   d''8 (   b'8    a'8  -) }     
\repeat volta 2 {   b'4. ^"~"    b'4 (   a'8  -)   g'4    a'8  \bar "|"   b'4. 
^"~"    b'8    a'8      b'8 (^\upbow   d''8  -)   b'8    a'8  \bar "|"   b'4. 
^"~"    b'4 (   a'8  -)   g'4    a'8 ( \bar "|"   b'4    d''8  -)   g''4 (   
e''8  -)   d''8 (   b'8    a'8  -) }   
}

\score{
    <<

	\context Staff="default"
	{
	    \voicedefault 
	}

    >>
	\layout {
	}
	\midi {}
}
