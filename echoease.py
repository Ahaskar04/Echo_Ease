import subprocess
from flask import Flask, jsonify, request
import subprocess

def convert_m4a_to_wav(m4a_file_path, wav_file_path):
    subprocess.run(['ffmpeg', '-i', m4a_file_path, wav_file_path])

convert_m4a_to_wav('first.m4a', 'first.wav')

import librosa
import librosa.display
import numpy as np
import pywt
import json
import ssl
import os

# Assume 'file_path' is the path to your .wav file, provided by your app
file_path = 'first.wav'

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Disable SSL certificate verification if needed
def allow_self_signed_https(allowed):
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

def convert_m4a_to_wav(m4a_file_path, wav_file_path):
    subprocess.run(['ffmpeg', '-i', m4a_file_path, wav_file_path], check=True)

@app.route('/api/process_audio', methods=['POST'])

def process_audio():
    # Example assumes a file path is provided in the request; adjust as needed for your application
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Save the file to a temporary file or directory
    m4a_file_path = os.path.join('/tmp', file.filename)
    file.save(m4a_file_path)

    wav_file_path = file_path.replace('.m4a', '.wav')
    convert_m4a_to_wav(file_path, wav_file_path)

    # Load the WAV file
    audio_data, sample_rate = librosa.load(wav_file_path, sr=None)

    # Feature extraction (simplified for brevity)
    spectral_centroid_mean = np.mean(librosa.feature.spectral_centroid(y=audio_data, sr=sample_rate))
    rolloff_mean = np.mean(librosa.feature.spectral_rolloff(y=audio_data, sr=sample_rate))
    zcr_mean = np.mean(librosa.feature.zero_crossing_rate(audio_data))

    # Assuming more feature extraction here...

    # Prepare data for external API request (example)
    data = {
        "features": {
            "spectral_centroid_mean": spectral_centroid_mean,
            "rolloff_mean": rolloff_mean,
            "zcr_mean": zcr_mean
            # Include more features as needed
        }
    }

    # This is where you'd make an external API request if needed, using `urllib.request` or similar
    # Skipping actual request for brevity

    return jsonify(data)

if __name__ == '__main__':
    allow_self_signed_https(True)  # Only if you need to bypass SSL verification
    app.run(debug=True, port=5000)

# Load the WAV file
audio_data, sample_rate = librosa.load(file_path, sr=None)

# Print audio data and sample rate
print(f"Audio data shape: {audio_data.shape}")
print(f"Sample rate: {sample_rate}")

# Define the parameters for framing and overlapping
frame_size = 1024  # Desired frame size in samples
hop_length = 512     # Desired hop size in samples

# Initialize a list to store frames
frames = []

# Check if audio data is long enough for framing
if len(audio_data) >= frame_size:
    # Calculate frames with overlapping
    frames = librosa.util.frame(audio_data, frame_length=frame_size, hop_length=hop_length).T
else:
    print("Audio duration too short.")

    # Apply Hamming window to each frame
windowed_frames = librosa.util.frame(audio_data, frame_length=frame_size, hop_length=hop_length).T * np.hamming(frame_size)

# Apply FFT to each windowed frame and keep only the first half of the spectrum
fft_frames = np.fft.rfft(windowed_frames, axis=1)

# MFCC parameters, as used during training
n_mfcc = 13  # Number of MFCC coefficients to extract
n_fft = 2048  # FFT window size in samples
hop_length = 512  # Hop length in samples
max_frames = 100  # The fixed number of frames per sample, as used during model training

# Extract MFCCs
mfccs = librosa.feature.mfcc(y=audio_data, sr=sample_rate, n_mfcc=n_mfcc, n_fft=n_fft, hop_length=hop_length)

# Pad or truncate the MFCCs to match 'max_frames'
if mfccs.shape[1] < max_frames:
    # If fewer frames, pad with zeros
    mfccs_padded = np.pad(mfccs, ((0, 0), (0, max_frames - mfccs.shape[1])), 'constant', constant_values=(0))
else:
    # If more frames, truncate
    mfccs_padded = mfccs[:, :max_frames]

# Flatten the padded/truncated MFCC matrix to a 1D array if needed for your model input
mfccs_flattened = mfccs_padded.flatten()

# 'mfccs_flattened' can now be used as input for your model, ensuring consistency with the training data structure


# Define the hop length for the spectral centroid calculation
hop_length = 512  # You can adjust this value as needed

# Calculate the spectral centroid for the audio file
spectral_centroid = librosa.feature.spectral_centroid(y=audio_data, sr=sample_rate, hop_length=hop_length)

# Compute the mean of the spectral centroid (to get a single value for the file)
spectral_centroid_mean = np.mean(spectral_centroid)

# Now, 'spectral_centroid_mean' contains the mean spectral centroid value for the .wav file
print(spectral_centroid_mean)


# Define the parameters for spectral roll-off
hop_length = 512  # You can adjust this value as needed
roll_percent = 0.85  # Spectral roll-off percentage

# Calculate the spectral roll-off
rolloff = librosa.feature.spectral_rolloff(y=audio_data, sr=sample_rate, hop_length=hop_length, roll_percent=roll_percent)

# Compute the mean of the spectral roll-off (to get a single value for the file)
rolloff_mean = np.mean(rolloff)

# 'rolloff_mean' contains the mean spectral roll-off value for the .wav file
print(rolloff_mean)


# Calculate the zero crossing rate
zcr = librosa.feature.zero_crossing_rate(audio_data)[0]

# Compute the mean of the zero crossing rate (to get a single value for the file)
zcr_mean = np.mean(zcr)

# 'zcr_mean' contains the mean zero crossing rate value for the .wav file
print(zcr_mean)



# Calculate MFCCs
mfccs = librosa.feature.mfcc(y=audio_data, sr=sample_rate, n_mfcc=13)

# Calculate the delta (first-order difference) of MFCCs
delta_mfccs = librosa.feature.delta(mfccs)

# Calculate the mean of the delta MFCCs across all frames
delta_mfccs_mean = np.mean(delta_mfccs, axis=1)

# 'delta_mfccs_mean' now contains the mean value of each delta MFCC across the time frames
# To get a single mean value that represents the overall average of these delta values, you can calculate the mean again across the coefficient means
overall_delta_mfcc_mean = np.mean(delta_mfccs_mean)

print(overall_delta_mfcc_mean)
# Calculate MFCCs
mfccs = librosa.feature.mfcc(y=audio_data, sr=sample_rate, n_mfcc=13)

# Calculate the delta (first-order difference) of MFCCs
delta_mfccs = librosa.feature.delta(mfccs)

# Calculate the mean of the delta MFCCs across all frames
delta_mfccs_mean = np.mean(delta_mfccs, axis=1)

# 'delta_mfccs_mean' now contains the mean value of each delta MFCC across the time frames
# To get a single mean value that represents the overall average of these delta values, you can calculate the mean again across the coefficient means
overall_delta_mfcc_mean = np.mean(delta_mfccs_mean)

print(overall_delta_mfcc_mean)



import pywt
# Perform a Discrete Wavelet Transform (DWT) - using Daubechies 4 ('db4')
# Adjust the level of decomposition based on your audio length and requirements
coeffs = pywt.wavedec(audio_data, 'db4', level=5)

# Flatten the coefficients to create a single feature vector
coeffs_flattened = np.hstack(coeffs)

# Calculate summary statistics of the coefficients
wavelet_mean = np.mean(coeffs_flattened)
wavelet_std = np.std(coeffs_flattened)

# 'wavelet_mean' contains the mean of the wavelet coefficients for the .wav file
# 'wavelet_std' contains the standard deviation of the wavelet coefficients for the .wav file
print(wavelet_mean, '\n', wavelet_std)


# Define the LPC order
lpc_order = 10

# Compute LPC coefficients
lpc_coeffs = librosa.lpc(audio_data, order=lpc_order)

# Calculate a derived feature from LPC coefficients, for example, the mean
lpc_mean = np.mean(lpc_coeffs)

# 'lpc_mean' contains the mean of the LPC coefficients for the .wav file
print(lpc_mean)


import urllib.request
import json
import os
import ssl

def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

# Request data goes here
# The example below assumes JSON formatting which may be updated
# depending on the format your endpoint expects.
# More information can be found here:
# https://docs.microsoft.com/azure/machine-learning/how-to-deploy-advanced-entry-script
data =  {
  "input_data": {
    "columns": [
      "0",
      "1",
      "2",
      "3",
      "4",
      "5",
      "6",
      "7",
      "8",
      "9",
      "10",
      "11",
      "12",
      "Spectral Centroid",
      "Spectral Roll-off",
      "Zero Crossing Rate",
      "Delta MFCC Mean",
      "Wavelet Mean",
      "Wavelet STD",
      "LPC Mean"
    ],
    "index": [0],
    "data": [{
        "0": float(mfccs_flattened[0]),
        "1": float(mfccs_flattened[1]),
        "2": float(mfccs_flattened[2]),
        "3": float(mfccs_flattened[3]),
        "4": float(mfccs_flattened[4]),
        "5": float(mfccs_flattened[5]),
        "6": float(mfccs_flattened[6]),
        "7": float(mfccs_flattened[7]),
        "8": float(mfccs_flattened[8]),
        "9": float(mfccs_flattened[9]),
        "10": float(mfccs_flattened[10]),
        "11": float(mfccs_flattened[11]),
        "12": float(mfccs_flattened[12]),
        "Spectral Centroid": float(spectral_centroid_mean),
        "Spectral Roll-off": float(rolloff_mean),
        "Zero Crossing Rate": float(zcr_mean),
        "Delta MFCC Mean": float(overall_delta_mfcc_mean),
        "Wavelet Mean": float(wavelet_mean),
        "Wavelet STD": float(wavelet_std),
        "LPC Mean": float(lpc_mean)
    }]
  }
}

body = str.encode(json.dumps(data))

url = 'https://echoease-wkgaa.southeastasia.inference.ml.azure.com/score'
# Replace this with the primary/secondary key or AMLToken for the endpoint
api_key = 'GmU95OZKWEUcDIA1fmQ3p2AiFSfuSQ7d'
if not api_key:
    raise Exception("A key should be provided to invoke the endpoint")

# The azureml-model-deployment header will force the request to go to a specific deployment.
# Remove this header to have the request observe the endpoint traffic rules
headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key), 'azureml-model-deployment': 'echoeasemk2-1' }

req = urllib.request.Request(url, body, headers)

try:
    response = urllib.request.urlopen(req)

    result = response.read()
    print(result)
except urllib.error.HTTPError as error:
    print("The request failed with status code: " + str(error.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(error.info())
    print(error.read().decode("utf8", 'ignore'))