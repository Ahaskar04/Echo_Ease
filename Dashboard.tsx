// Dashboard.tsx
import React, { useState } from "react";
import {
  View,
  Text,
  StyleSheet,
  ImageBackground,
  Image,
  TouchableOpacity,
  StatusBar,
  Alert,
  ScrollView,
} from "react-native";
import { useNavigation } from "@react-navigation/native";
import { StackNavigationProp } from "@react-navigation/stack";
import { RootStackParamList } from "./App"; // Make sure this import path is correct
import { Audio } from "expo-av";
import * as FileSystem from "expo-file-system";
import axios from "axios";
import { FLASK_API_URL } from "@env";

type DashboardScreenNavigationProp = StackNavigationProp<
  RootStackParamList,
  "Dashboard"
>;

const DashboardScreen: React.FC = () => {
  const navigation = useNavigation<DashboardScreenNavigationProp>();
  const [recording, setRecording] = useState<Audio.Recording | null>(null);
  const [isRecording, setIsRecording] = useState(false);
  const [savedRecordings, setSavedRecordings] = useState<
    Array<{ uri: string; name: string }>
  >([]);

  const handleMicrophonePress = async () => {
    if (isRecording) {
      setIsRecording(false);
      await stopRecording();
    } else {
      setIsRecording(true);
      await startRecording();
    }
  };

  async function startRecording() {
    try {
      const permissionResponse = await Audio.requestPermissionsAsync();
      if (permissionResponse.status !== "granted") {
        Alert.alert(
          "Permissions required",
          "Please grant microphone access to use this feature."
        );
        setIsRecording(false);
        return;
      }
      await Audio.setAudioModeAsync({
        allowsRecordingIOS: true,
        playsInSilentModeIOS: true,
      });
      const { recording: newRecording } = await Audio.Recording.createAsync(
        Audio.RecordingOptionsPresets.HIGH_QUALITY
      );
      setRecording(newRecording);
    } catch (err) {
      setIsRecording(false);
      console.error("Failed to start recording", err);
    }
  }

  async function stopRecording() {
    if (!recording) {
      return;
    }
    await recording.stopAndUnloadAsync();
    await Audio.setAudioModeAsync({
      allowsRecordingIOS: false,
    });
    const uri = recording.getURI();
    setRecording(null);

    if (uri) {
      const fileUri = `${
        FileSystem.documentDirectory
      }${new Date().toISOString()}.m4a`;
      try {
        await FileSystem.moveAsync({ from: uri, to: fileUri });
        const recordingInfo = {
          uri: fileUri,
          name: `Recording ${new Date().toISOString()}`,
        };
        setSavedRecordings((prev) => [...prev, recordingInfo]);
        console.log("Recording saved to", fileUri);
      } catch (error) {
        console.error("Error saving recording", error);
      }
      await uploadAudio(fileUri);
    }
  }

  async function playRecording(fileUri: string) {
    const { sound } = await Audio.Sound.createAsync({ uri: fileUri });
    await sound.playAsync();
  }

  const uploadAudio = async (fileUri: string) => {
    const formData = new FormData();
    formData.append("file", {
      uri: fileUri,
      type: "audio/m4a",
      name: "recording.m4a",
    } as any);

    try {
      const response = await axios.post(FLASK_API_URL, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        timeout: 60000,
      });
      console.log("Upload successful", response.data);
    } catch (error) {
      console.error("Upload failed", error);
    }
  };

  const handleProfileButton = () => {
    navigation.navigate("Settings");
  };
  const handleGoBack = () => {
    navigation.goBack();
  };
  const handleResultsPress = () => {
    navigation.navigate("Result");
  };

  return (
    <View style={styles.container}>
      <StatusBar barStyle="light-content" />
      <ImageBackground
        source={require("./assets/Bg11.png")}
        style={styles.background}
      >
        <View style={styles.header}>
          <TouchableOpacity onPress={handleGoBack} style={styles.backButton}>
            <Image
              source={require("./assets/backbutton.png")}
              style={styles.backButtonIcon}
            />
          </TouchableOpacity>
          <Text style={styles.welcomeText}>Welcome back!</Text>
        </View>

        {/* Microphone button */}
        <TouchableOpacity
          style={[
            styles.microphoneButton,
            isRecording && { backgroundColor: "red" },
          ]} // Change color when recording
          onPress={handleMicrophonePress}
        >
          <Image
            source={require("./assets/Microphone.png")}
            style={styles.microphoneIcon}
          />
        </TouchableOpacity>
        <Text style={styles.readyToListenText}>
          {isRecording ? "Recording..." : "Ready to listen!"}
        </Text>

        <View style={styles.footerContainer}>
          <TouchableOpacity style={styles.footerButton}>
            <Image
              source={require("./assets/home.png")}
              style={styles.footerHomeIcon}
            />
          </TouchableOpacity>
          <TouchableOpacity style={styles.footerButton}>
            <Image
              source={require("./assets/stats.png")}
              style={styles.footerStatsIcon}
            />
          </TouchableOpacity>
          <TouchableOpacity
            onPress={handleProfileButton}
            style={styles.footerButton}
          >
            <Image
              source={require("./assets/profile.png")}
              style={styles.footerProfileIcon}
            />
          </TouchableOpacity>
          <TouchableOpacity
            onPress={handleResultsPress}
            style={styles.footerButton}
          >
            <Image
              source={require("./assets/results.png")}
              style={styles.footerSettingsIcon}
            />
          </TouchableOpacity>
        </View>
        <View style={{ alignItems: "center", marginTop: 20 }}>
          <Text style={{ fontWeight: "bold", fontSize: 20, color: "#fff" }}>
            Saved Recordings:
          </Text>
          <ScrollView style={{ maxHeight: 200, width: "100%", marginTop: 10 }}>
            {savedRecordings.map((recording, index) => (
              <TouchableOpacity
                key={index}
                style={{
                  backgroundColor: "#ddd",
                  padding: 10,
                  marginVertical: 5,
                  borderRadius: 5,
                }}
                onPress={() => playRecording(recording.uri)}
              >
                <Text style={{ color: "#000" }}>{recording.name}</Text>
              </TouchableOpacity>
            ))}
          </ScrollView>
        </View>

        <View style={styles.footerContainer}>
          {/* Footer content remains unchanged */}
        </View>
      </ImageBackground>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  background: {
    flex: 1,
    resizeMode: "cover",
    alignItems: "center",
    justifyContent: "space-between",
  },
  header: {
    width: "100%",
    padding: 20,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    marginTop: 20,
  },
  backButton: {
    position: "absolute",
    top: 50,
    left: 30,
    // Style for the back button
  },
  welcomeText: {
    fontSize: 24,
    fontWeight: "bold",
    color: "#FFFFFF",
    position: "absolute",
    top: 100,
    left: 70,
    // Add additional styling as needed
  },
  microphoneButton: {
    width: 250, // Adjust size as needed
    height: 250, // Adjust size as needed
    borderRadius: 130, // Make it round
    backgroundColor: "#6F58ED", // Background color for the button
    justifyContent: "center",
    alignItems: "center",
    position: "absolute",
    top: 300,
  },
  microphoneIcon: {
    width: 75, // Adjust size as needed
    height: 75, // Adjust size as needed
  },
  readyToListenText: {
    fontSize: 22,
    fontWeight: "bold",
    color: "#6338C5",
    marginBottom: 20, // Adjust distance from the bottom as needed
    position: "absolute",
    top: 600,
  },
  footerContainer: {
    flexDirection: "row",
    justifyContent: "space-evenly",
    alignItems: "center",
    backgroundColor: "#6F58ED", // Set your preferred background color
    paddingVertical: 10, // Adjust padding to your preference
    paddingHorizontal: 10, // Adjust horizontal padding as needed
    position: "absolute", // Position at the bottom
    bottom: 40,
    left: 20,
    right: 20,
    borderRadius: 24,
    zIndex: 1,
  },
  footerButton: {
    // Optional, if you want to style the touchable area
    padding: 10, // Padding for touchable area, adjust as needed
  },
  backButtonIcon: {
    width: 15,
    height: 15,
  },
  footerHomeIcon: {
    width: 26, // Adjust size as needed
    height: 25,
  },
  footerStatsIcon: {
    width: 22, // Adjust size as needed
    height: 21,
  },
  footerProfileIcon: {
    width: 22, // Adjust size as needed
    height: 23,
  },
  footerSettingsIcon: {
    width: 19, // Adjust size as needed
    height: 24,
  },
  // Icons in footer would have styles if needed
});

export default DashboardScreen;
