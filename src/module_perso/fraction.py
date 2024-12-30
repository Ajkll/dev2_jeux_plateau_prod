class NullDenominatorValueException(Exception):
    """den as we declared it in Fraction is null"""

    pass


class InvalidOperandTypeException(TypeError):
    """invalid type is used in a Fraction operation"""

    pass


def _gcd(a: int, b: int) -> int:
    """Calculate GCD using the recursive Euclidean algorithm"""
    return abs(a) if b == 0 else _gcd(b, a % b)


class Fraction:
    """Class representing a fraction and operations on it.
    Updated by J.Alexis : 12/12/2024
    Author : V. Van den Schrieck
    Date : October 2021
    This class allows fraction manipulations through several operations.
    """

    def __init__(self, num: int = 0, den: int = 1):
        """Initialize a fraction and reduce it to its simplest form.

        PRE - Args:
            num is a INT
            den is a INT

        POST - The fraction is reduced to its simplest --int form.

        Raises:
            NullDenominatorValueException: Note an real number cannot be divided by zero by arithmethic operations.
        """
        if den == 0:
            raise NullDenominatorValueException("Denominator cannot be zero.")
        if den < 0:
            num, den = -num, -den

        gcd = _gcd(num, den)
        self._num = num // gcd
        self._den = den // gcd

    @property
    def numerator(self) -> int:
        """
        methode to acces our private attribute _num

        PRE-
        POST -  Method get int-- the numerator of the fraction is returned
        """
        return self._num

    @property
    def denominator(self) -> int:
        """
        method to acces our private attribute _den

        PRE-
        POST - Method get int-- the denominator of the fraction is returned
        """
        return self._den

    def __str__(self) -> str:
        """
        give description as str form of our reduced fraction form

        Pre -
        Post - for our object fraction str -- description ofthe fraction is returned

        """
        return (
            "1"
            if self._num == self._den
            else str(self._num) if self._den == 1 else f"{self._num}/{self._den}"
        )

    def as_mixed_number(self) -> str:
        """
        Convert the fraction to a mixed number string representation

        PRE -
        POST - Returns the mixed number representation as a string
            Returns str-- "whole remainder/denominator" if non valid fraction
            Returns str-- "num/den" if valid fraction
            Returns str-- 0 for a zero fraction

        """
        sign = "-" if self._num * self._den < 0 else ""
        numerator, denominator = abs(self._num), abs(self._den)
        whole = numerator // denominator
        remainder = numerator % denominator

        if whole == 0 and remainder == 0:
            return "0"

        if remainder == 0:
            return f"{sign}{whole}"

        if whole == 0:
            return f"{sign}{numerator}/{denominator}"

        return f"{sign}{whole} {remainder}/{denominator}"

    def _check_fraction_or_int(self, another_fraction) -> "Fraction":
        """
        check if arg is int or Fraction value or another_fraction

        PRE -
        POST - Returns a Fraction instance:
            if arg "another_fraction" is --int it is converted to a Fraction with den equal to 1
            if arg "another_fraction" is already a Fraction as we have declare a fraction should be then we return it back

        Raises - TypeError if "another_fraction is neither an int or a Fraction
        """
        if isinstance(another_fraction, bool):
            raise InvalidOperandTypeException(
                "expected to be either fraction or int arg"
            )
        if isinstance(another_fraction, int):
            return Fraction(another_fraction)
        if not isinstance(another_fraction, Fraction):
            raise InvalidOperandTypeException(
                "expected to be either fraction or int arg"
            )
        return another_fraction

    def __add__(self, another_fraction) -> "Fraction":
        """
        Add two fractions

        PRE -

        POST - Returns a Fraction instance:
            Return the addition of two fractions

        """
        another_fraction = self._check_fraction_or_int(another_fraction)
        return Fraction(
            self._num * another_fraction._den + another_fraction._num * self._den,
            self._den * another_fraction._den,
        )

    def __sub__(self, another_fraction) -> "Fraction":
        """
        substract two fractions

        PRE -

        POST - Returns a Fraction instance:
            Return the substraction of two fractions

        """
        another_fraction = self._check_fraction_or_int(another_fraction)
        return Fraction(
            self._num * another_fraction._den - another_fraction._num * self._den,
            self._den * another_fraction._den,
        )

    def __mul__(self, another_fraction) -> "Fraction":
        """
        Multiply two fractions

        PRE -

        POST - Returns a Fraction instance:
            Return the multiplication of two fractions

        """
        another_fraction = self._check_fraction_or_int(another_fraction)
        return Fraction(
            self._num * another_fraction._num, self._den * another_fraction._den
        )

    def __truediv__(self, another_fraction) -> "Fraction":
        """
        Divides two fractions.

        PRE -

        POST - Returns a Fraction instance:
            Return the division of two fractions.

        Raises:
            ZeroDivisionError: if "another_fraction" is 0 (denominator or numerator).
        """
        another_fraction = self._check_fraction_or_int(another_fraction)
        if another_fraction._num == 0:
            raise ZeroDivisionError("Division by zero is not allowed")

        result = Fraction(
            self._num * another_fraction._den, self._den * another_fraction._num
        )
        return result

    def __pow__(self, power: int) -> "Fraction":
        """
        Raise the fraction to an integer power.

        PRE -

        POST - Returns a Fraction instance:
            Return the fraction raised to the given power.

        Raises:
            ValueError: if power is not an integer.
        """
        if not isinstance(power, int):
            raise ValueError("Power must be an integer")

        if power == 0:
            return Fraction(1, 1)

        if power < 0:
            if self._num == 0:
                raise ZeroDivisionError("Cannot raise zero to a negative power")
            return Fraction(self._den ** abs(power), self._num ** abs(power))

        result = Fraction(self._num**power, self._den**power)
        return result

    def __eq__(self, another_fraction) -> bool:
        """
        Check if two fractions are equales.

        PRE -

        POST - Returns a bool:
            Return true if th two fractions are equales or false otherwise

        """
        another_fraction = self._check_fraction_or_int(another_fraction)
        return self._num * another_fraction._den == another_fraction._num * self._den

    def __float__(self) -> float:
        """
        give the float value of the fraction


        PRE -

        POST - Returns a float:
            Return the float value of the fraction


        """
        return self._num / self._den

    def __lt__(self, another_fraction) -> bool:
        """
        Overloading - advice if one fraction is smaller than another

        PRE -
        POST - Returns a bool:
            return true if one fraction is smaller than another, otherwise false
        """
        # Utilisation de _check_fraction_or_int pour vérifier et convertir l'argument
        another_fraction = self._check_fraction_or_int(another_fraction)
        return self._num * another_fraction._den < another_fraction._num * self._den

    def __le__(self, another_fraction) -> bool:
        """
        Overloading - advice if one fraction is smaller or equales to another

        PRE -

        Post - Returns a bool:
            return true if one fraction is smaller or equales to another otherwise false

        """
        another_fraction = self._check_fraction_or_int(another_fraction)
        return self._num * another_fraction._den <= another_fraction._num * self._den

    def __abs__(self) -> "Fraction":
        """
        Return the absolute value of the fraction.

        PRE -

        POST - Returns a Fraction instance:
            Return the fraction with a positive num


        """
        return Fraction(abs(self._num), self._den)

    def is_zero(self) -> bool:
        """

        Check if the fraction is equal to zero

        PRE -

        POST - Returns a bool:
            Return true if the fraction is equal to zero otherwise false


        """
        return self._num == 0

    def is_integer(self) -> bool:
        """

        Check if the fraction is an integer or not

        PRE -

        POST - Returns a bool:
            Return true if the fraction is an integer otherwise false


        """
        return self._den == 1

    def is_proper(self) -> bool:
        """
        Check if abs(fraction) is smaller than 1

        PRE -

        POST - Returns a bool:
            Return true if abs(fraction) is smaller than 1 otherwise false


        """
        return abs(self._num) < abs(self._den)

    def is_unit(self) -> bool:
        """
        Determine whether the fraction is a unit fraction, meaning its numerator is ±1

        PRE -

        POST - Returns a bool:
            Return true if the fraction is a unit fraction otherwise false

        """
        return abs(self._num) == 1 and self._den > 1

    def __ge__(self, another_fraction):
        """
        Overloading of the >= operator for our class fractions

        PRE -

        POST - Returns a bool:
            Return True if self is greater or equal than another_fraction, False otherwise
        """
        another_fraction = self._check_fraction_or_int(another_fraction)
        return self._num * another_fraction._den >= another_fraction._num * self._den

    def __gt__(self, another_fraction):
        """
        Overloading of the > operator for our class fractions

        PRE -

        POST - Returns a bool:
            Return True if self is greater  than another_fraction, False otehrwise
        """
        another_fraction = self._check_fraction_or_int(another_fraction)
        return self._num * another_fraction._den > another_fraction._num * self._den
