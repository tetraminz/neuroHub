# Dataset Name

bigP3BCI v1.0.0

# Privacy Note

The dataset has no personal identifiers. Per institutional restrictions, source data files (in BCI2000 .dat format) cannot be publicly distributed as they potentially contain identifiable information. 


# Experimental Protocol

This dataset represents a collection of data generated from previous online studies to improve a P300-based brain-computer interface (BCI) for communication.
In the BCI studies, all participants performed copy-spelling of predefined tokens (words or number sequence) using the P300 speller. During copy-spelling, the user spells a token and is provided a cue on which new character to spell. A user is presented with a set of choices on a speller interface in a matrix layout (6 x 6 or 9 x 8 grid); for R x C, R is the number of rows and C is the number of columns in the matrix layout. To select a character, the user focuses on that target character as subsets of characters are illuminated on the screen and electroenchephalography (EEG) signals are being measured. The illumination of a character subset represents a visual stimulus event. The BCI infers the user’s target character by processing the EEG data to predict whether the target character was present in a group of illuminated characters and selecting the character with the maximum cumulative response as the user’s target character estimate.  
A P300 speller experiment session consists of a calibration phase and a test phase. During the calibration phase, participants perform copy-spelling with no classifier use and no BCI feedback presented to collect labeled EEG data to train a P300 classifier. During the test phase, the trained P300 classifier is applied and participants perform copy-spelling with the BCI prediction of the target character presented as feedback after data collection for a character trial.
Data were recorded using BCI2000. EEG signals were collected at 256 Hz using passive gel-based  or active dry electrodes connected to biosignal amplifiers (g.tec medical engineering GmbH). An electrode impedance check was conducted to ensure low impedance (generally < 40 k$\Omega$). Raw EEG data were bandpass filtered and when applicable, notch filtered to remove electrical noise; all filtering were performed at the biosignal amplifier stage (https://www.bci2000.org/mediawiki/index.php/User_Reference:gUSBampADC). 
For hybrid BCI use, eye gaze position, eye position, eye distance from the screen and pupil diameter were collected using a Tobii Pro X2-30 (Tobii AB) infrared eye tracker. The eye tracker was calibrated for each participant prior to BCI use. Eye tracker data were acquired via the EyeTrackerLogger filter in BCI2000 and synchronised to EEG data collection during BCI use. Raw eye tracker data were preprocessed based on the technical specifications of the Tobii EyeTrackerLogger filter in BCI2000 (https://www.bci2000.org/mediawiki/index.php/Contributions:EyetrackerLogger).


# Data Format

The data are provided in EDF+ files. 
Files are organised by study. The base hierarchy levels are Study&\&_$$\SE@@@, where #, $$ and @@@ are the study, subject and session identifiers, respectively. The next hierarchy level specifies either the ~\Train or ~\Test phase of the experiment. The subsequent hierarchy levels until the data files depend on the number of conditions tested during the experiment. 


# Funding

Dataset development was funded by a grant supplement from the National Institute on Deafness and Other Communication Disorders at the National Institutes of Health (R21DC018347-02S1).
