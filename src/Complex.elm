module Complex (complex,i,one,zero,real,imaginary, fromReal,abs,mult) where

{-| The complex module gives you most of what you could desire to use complex numbers. There is not much else to say. 


-}


type alias Complex = {re: Float, im: Float}
{-| Generates a complex number. 

complex 1 2 = 1+2i

-}
complex : Float -> Float -> Complex
complex a b = {re = a, im = b}

i : Complex
i = {re = 0, im = 1}
{-| The number 1.

-}
one : Complex
one = {re = 1, im = 0}
{-| The number 0.

-}

zero : Complex
zero = {re = 0, im = 0}

{-| Provides the real part of a complex number. 

-}

real : Complex -> Float
real c = c.re


{-| Provides the imaginary part of a complex number.

-}

imaginary : Complex -> Float
imaginary c = c.im



{-| Creates a complex number from one real numer. So fromReal 5 = 5 + 0i

-}

fromReal : Float -> Complex
fromReal r = 
  {re = r, im = 0}


{-| Takes the absolute value of a complex number.


-}

abs : Complex -> Float 
abs c = 
  (c.re^2 + c.im^2)^(0.5)


{-| Returns the conjugate of a complex number e.g conjugate 2+3i = 2 - 3i

-}

conjugage : Complex -> Complex
conjugage c1 = 
  {re = c1.re, im = (-1)*c1.im}


{-| Negates a complex number. E.g negation 1+2i = -1-2i

-}

negation : Complex -> Complex
negation c = 
  {re = (-1) * c.re, im = (-1) * c.im}


{-| Adds two complex numbers

-}
add : Complex -> Complex -> Complex
add c1 c2 = 
  {re = (c1.re + c2.re), im = (c1.im + c2.im)}

{-|Subtacts two complex numbers.

-}

sub : Complex -> Complex -> Complex
sub c1 c2 = add c1 (negation c2)

{-| Multiplies two complex numbers

-}
mult : Complex -> Complex -> Complex
mult c1 c2 = 
  {re = c1.re * c2.re - (c1.im * c2.im), im = c1.re * c2.im + c2.re * c1.im}

{-| Divides two complex numbers.

-}
div : Complex -> Complex -> Complex 
div c1 c2 = 
  let
    numRe = c1.re * c2.re + c1.im * c2.im
    numIm = c1.im * c2.re - c1.re * c2.im
    den = c2.re^2 + c2.im^2
  in 
    {re = numRe/den, im = numIm/den}



sgn : Complex -> Float
sgn c = 
  case (c.re, c.im) of 
    (0,0) -> 0 
    (0,b) -> if b > 0 then (1) else if b < 0 then (-1) else 0
    (a,b) -> if a > 0 then 1 else (-1)


{-| Square root of a complex number. Returns both possibilites.

-}
sqrt : Complex -> (Complex, Complex)
sqrt c1 = 
  let
  gamma = ((c1.re + (abs c1)) /2)^(0.5)
  delta = (((-1) * c1.re + (abs c1)) /2)^(0.5)
  in
    ({re=gamma, im=delta}, {re = (-1)*gamma, im = (-1)* delta})


{-| A really well made version of atan to be used in the argument. Don't export.

-}
--https://hackage.haskell.org/package/base-4.8.2.0/docs/src/GHC.Float.html#atan2
atan2 : number -> number' -> Float
atan2 y x = 
  if x > 0 then atan (y/x)
  else if x == 0 && y > 0 then pi / 2
  else if x < 0 && y > 0 then pi + atan (y/x)
  else if (x <= 0 && y < 0 ) then 0 - (atan2 (-y) x)
  else if (y == 0 && (x < 0)) then pi
  else if x == 0 && y == 0 then y
  else x+y
  


{-| The argument of a complex number. It is in radians

-}
arg : Complex -> Float
arg c = 
  case (c.re, c.im) of 
    (0,0) -> 0 
    (x,y) -> atan2 y x

{-| The natrual log of a complex number

-}

ln : Complex -> (Int -> Complex)
ln z = 
  \k -> {re = logBase (Basics.e) (abs z), im = (arg z) + 2 * Basics.pi * (toFloat k)}

{-| The exponent of a complex number.

-}
