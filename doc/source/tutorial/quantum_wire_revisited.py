# Physics background
# ------------------
#  Conductance of a quantum wire; subbands
#
# Kwant features highlighted
# --------------------------
#  - Using iterables and builder.HoppingKind for making systems
#  - introducing `reversed()` for the leads
#
# Note: Does the same as tutorial1a.py, but using other features of kwant

#HIDDEN_BEGIN_xkzy
import kwant

# For plotting
from matplotlib import pyplot


def make_system(a=1, t=1.0, W=10, L=30):
    # Start with an empty tight-binding system and a single square lattice.
    # `a` is the lattice constant (by default set to 1 for simplicity.
    lat = kwant.lattice.square(a)

    sys = kwant.Builder()
#HIDDEN_END_xkzy

    #### Define the scattering region. ####
#HIDDEN_BEGIN_vvjt
    sys[(lat(x, y) for x in range(L) for y in range(W))] = 4 * t
#HIDDEN_END_vvjt
#HIDDEN_BEGIN_nooi
    sys[lat.nearest] = -t
#HIDDEN_END_nooi

    #### Define the leads. ####
    # First the lead to the left, ...
    # (Note: TranslationalSymmetry takes a real-space vector)
#HIDDEN_BEGIN_iepx
    sym_lead0 = kwant.TranslationalSymmetry((-a, 0))
    lead0 = kwant.Builder(sym_lead0)

    lead0[(lat(0, j) for j in xrange(W))] = 4 * t
    lead0[lat.nearest] = -t
#HIDDEN_END_iepx

    # ... then the lead to the right.  We use a method that returns a copy of
    # `lead0` with its direction reversed.
#HIDDEN_BEGIN_xkdo
    lead1 = lead0.reversed()
#HIDDEN_END_xkdo

    #### Attach the leads and return the system. ####
#HIDDEN_BEGIN_yxot
    sys.attach_lead(lead0)
    sys.attach_lead(lead1)

    return sys
#HIDDEN_END_yxot


#HIDDEN_BEGIN_ayuk
def plot_conductance(sys, energies):
    # Compute conductance
    data = []
    for energy in energies:
        smatrix = kwant.solve(sys, energy)
        data.append(smatrix.transmission(1, 0))

    pyplot.figure()
    pyplot.plot(energies, data)
    pyplot.xlabel("energy [in units of t]")
    pyplot.ylabel("conductance [in units of e^2/h]")
    pyplot.show()
#HIDDEN_END_ayuk


#HIDDEN_BEGIN_cjel
def main():
    sys = make_system()

    # Check that the system looks as intended.
    kwant.plot(sys)

    # Finalize the system.
    sys = sys.finalized()

    # We should see conductance steps.
    plot_conductance(sys, energies=[0.01 * i for i in xrange(100)])
#HIDDEN_END_cjel


# Call the main function if the script gets executed (as opposed to imported).
# See <http://docs.python.org/library/__main__.html>.
#HIDDEN_BEGIN_ypbj
if __name__ == '__main__':
    main()
#HIDDEN_END_ypbj
