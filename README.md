# RC-Interpretability
Does activation patching identify localized computational structure in reservoir computers, and does that structure correspond to what we know about network topology?

Reservoir computers offer a rare opportunity for interpretability research: a neural-network-like system where the underlying structure is fully known and controllable. Unlike transformers, where identifying a "circuit" requires inferring ground truth from behavior, reservoir networks can be constructed with known topology, thinned in controlled ways, and analyzed against established performance metrics. This makes them a natural testbed for asking whether interpretability methods like activation patching actually recover true computational structure or just correlate with it.

Our toy problem will be predicting orbits on chaotic attractors, specifically the Lorenz, Rossler, and Thomas attractors. This is a task at which reservoir computers, particularly those with thinned networks, perform well.

# Step 0: Collecting our test subjects
This step is where we generate a set of reservoirs that perform well on the task of predicting orbits on a given attractor (we'll start with the Lorenz). Our metric for performing well is "valid prediction time", which is a measure of how long it takes the predicted trajectory to diverge a certain amount from the actual trajectory.

# Step 1: Identifying network structures and their contribution
The main goal here is to investigate the structure of the well-performing networks and how they contribute to the predictions. Are certain nodes or components of the network more dominant than others? Does this change over time? We also want a nice way to visualize this - some sort of heat map of the network would be ideal.
End product: Data on the responses of the network nodes and a visualization of that data, showing how the activity of a given node changes over the course of the prediction.

# Step 2: Test patching on specific subsets of the network
Now that we've identified which portions of a network contribute the most to the prediction process and which ones contribute the least, we can begin patching these to see how the valid prediction time is affected.
Each patching has four valid prediction times to compare:
- A clean run ($T_{clean}$). This is the prediction time from step 0, and the "good" baseline.
- A corrupted run ($T_{corr}$). This is the prediction time from a run with bad input data. This is the "bad" baseline.
- A patched run ($T_{patch}$). This is the prediction time from a run with bad input data, where the responses from the good run are patched in at specific times and nodes in the network.
- A null baseline ($T_{null}$). This is the prediction time from a run with bad input data with random noise patched in at the same place as $T_{patch}$. This is to control for the act of patching itself.
If $T_{patch} >> T_{null}$ and  $T_{patch} >> T_{corr}$, then that means that the portion we patched has a measurable influence on the valid prediction time.
End product: Data on how much patching certain components of the network affects the valid prediction time.

There are a few other questions to explore:
- What if the "bad" baseline is from another attractor? Say we give a reservoir trained to predict the Lorenz attractor an orbit from the Rossler attractor and ask it to predict it. Does patching in responses from a Lorenz run improve the valid prediction time, and by how much?
- What is the underlying math behind the observed phenomena? This is a later question, because we first have to observe the phenomena before we can really hypothesize about their causes. Prior results indicate (citations to literature needed) that the spectral radius of the network matrix influences the valid prediction time, but this is also dependent on the thinness of the network (Citation). Thinned networks perform better with large spectral radii, while dense networks fail to predict well when their spectral radius is too large, so the connectivity of the network and the sizes of its components also matter.
