"""
This module provides read/write access to the parallel port for Linux or Windows.

The :class:`~psychopy.parallel.Parallel` class described below will attempt to
load whichever parallel port driver is first found on your system and should
suffice in most instances. If you need to use a specific driver then, instead of
using :class:`~psychopy.parallel.ParallelPort` shown below you can use one of the following as
drop-in replacements, forcing the use of a specific driver:

    - `psychopy.parallel.PParallelInpOut32`
    - `psychopy.parallel.PParallelDLPortIO`
    - `psychopy.parallel.PParallelLinux`

Either way, each instance of the class can provide access to a different parallel
port.

There is also a legacy API which consists of the routines which are directly in this
module.  That API assumes you only ever want to use a single parallel port at once.
"""
from psychopy import logging
import sys

# To make life easier, only try drivers which have a hope in heck of working
if sys.platform.startswith('linux'):
    from _linux import PParallelLinux
    ParallelPort = PParallelLinux
elif sys.platform == 'win32':
    from ctypes import windll
    if hasattr(windll, 'inpout32'):
        from _inpout32 import PParallelInpOut32
        ParallelPort = PParallelInpOut32
    elif hasattr(windll, 'dlportio'):
        from _dlportio import PParallelDLPortIO
        ParallelPort = PParallelDLPortIO
    else:
        logging.warning("psychopy.parallel has been imported but no "
                        "parallel port driver found. Install either "
                        "input32 or dlportio")
else:
    logging.warning("psychopy.parallel has been imported on a Mac "
                    "(which doesn't have a parallel port?)")

    #OS X doesn't have a parallel port but write the class for doc purps
    class ParallelPort(object):
        """
        This class provides read/write access to the parallel port on Windows & Linux

        Usage::

            from psychopy import parallel
            port = parallel.ParallelPort(address=0x0378)
            port.setData(4)
            port.readPin(2)
            port.setPin(2, 1)
        """

        def __init__(self, address):
            """This is just a dummy constructor to avoid errors 
            when the parallel port cannot be initiated
            """

            logging.warning("psychopy.parallel has been imported but "
                        "(1) no parallel port driver could be found or accessed on Windows or"
                        "(2) PsychoPy is run on a Mac (without parallel-port support for now)")

        def setData(self, data):
            """
            Set the data to be presented on the parallel port (one ubyte).
            Alternatively you can set the value of each pin (data pins are pins
            2-9 inclusive) using :func:`~psychopy.parallel.setPin`

            examples::

                parallel.setData(0)  # sets all pins low
                parallel.setData(255)  # sets all pins high
                parallel.setData(2)  # sets just pin 3 high (remember that pin2=bit0)
                parallel.setData(3)  # sets just pins 2 and 3 high

            you can also convert base 2 to int v easily in python::

                parallel.setData( int("00000011",2) )#pins 2 and 3 high
                parallel.setData( int("00000101",2) )#pins 2 and 4 high
            """
            sys.stdout.flush()
            raise NotImplementedError("Parallel ports don't work on a Mac")

        def readData(self):
            """Return the value currently set on the data pins (2-9)"""
            raise NotImplementedError("Parallel ports don't work on a Mac")

        def readPin(self, pinNumber):
            """Determine whether a desired (input) pin is high(1) or low(0).

            Pins 2-13 and 15 are currently read here
            """
            raise NotImplementedError("Parallel ports don't work on a Mac")

# In order to maintain API compatibility, we have to manage to deal with
# the old, non-object-based, calls.  This necessitates keeping a
# global object referring to a port.  We initialise it the first time
# that the person calls
PORT = None  # don't create a port until necessary


def setPortAddress(address=0x0378):
    """
    Set the memory address or device node for your parallel port
    of your parallel port, to be used in subsequent commands

    common port addresses::

        LPT1 = 0x0378 or 0x03BC
        LPT2 = 0x0278 or 0x0378
        LPT3 = 0x0278

    or for Linux::
        /dev/parport0

    This routine will attempt to find a usable driver depending
    on your platform
    """

    global PORT
    if isinstance(address, basestring) and address.startswith('0x'): #convert u"0x0378" into 0x0378
        address = int(address, 16)

    # This is useful with the Linux-based driver where deleting
    # the port object ensures that we're not longer holding the
    # device node open and that we won't error if we end up
    # re-opening it
    if PORT is not None:
        del PORT

    try:
        PORT = ParallelPort(address=address)
    except Exception as exp:
        logging.warning('Could not initiate port: %s' % str(exp))
        PORT = None


def setData(data):
    """
    Set the data to be presented on the parallel port (one ubyte).
    Alternatively you can set the value of each pin (data pins are pins
    2-9 inclusive) using :func:`~psychopy.parallel.setPin`

    examples::

        parallel.setData(0) #sets all pins low
        parallel.setData(255) #sets all pins high
        parallel.setData(2) #sets just pin 3 high (remember that pin2=bit0)
        parallel.setData(3) #sets just pins 2 and 3 high

    you can also convert base 2 to int v easily in python::

        parallel.setData( int("00000011",2) )#pins 2 and 3 high
        parallel.setData( int("00000101",2) )#pins 2 and 4 high
    """

    global PORT
    if PORT is None:
        raise RuntimeError('Port address must be set using setPortAddress')
    PORT.setData(data)


def setPin(pinNumber, state):
    """Set a desired pin to be high(1) or low(0).

    Only pins 2-9 (incl) are normally used for data output::

        parallel.setPin(3, 1)#sets pin 3 high
        parallel.setPin(3, 0)#sets pin 3 low
    """
    global PORT
    PORT.setPin(pinNumber, state)


def readPin(pinNumber):
    """
    Determine whether a desired (input) pin is high(1) or low(0).

    Pins 2-13 and 15 are currently read here
    """
    global PORT
    return PORT.readPin(pinNumber)
