import React from "react";
import {
  View,
  Text,
  Image,
  StyleSheet,
  SafeAreaView,
  ImageBackground,
} from "react-native";
import { useNavigation } from "@react-navigation/native";
import { StackNavigationProp } from "@react-navigation/stack";
import { RootStackParamList } from "./App"; // Make sure this import path is correct

type ResultScreenNavigationProp = StackNavigationProp<
  RootStackParamList,
  "Result"
>;

const Results: React.FC = () => {
  const navigation = useNavigation<ResultScreenNavigationProp>();
  return (
    <SafeAreaView style={styles.container}>
      <ImageBackground
        source={require("./assets/Bg14.png")}
        style={styles.backgroundImage}
      >
        <View style={styles.header}></View>
        <Image source={require("./assets/Logo2.png")} style={styles.logo} />
        <Text style={styles.logoText}>EchoEase</Text>
      </ImageBackground>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  backgroundImage: {
    flex: 1,
    resizeMode: "cover", // or 'stretch'
  },
  header: {
    backgroundColor: "#7D34E3", // Replace with the color code of your header if it is not transparent
    height: "40%", // Adjust height according to your Figma design
    borderBottomRightRadius: 60, // Adjust the border radius according to your design
  },
  logo: {
    width: 100, // Set the width according to your logo's aspect ratio
    height: 100, // Set the height according to your logo's aspect ratio
    alignSelf: "center",
    position: "absolute",
    bottom: "20%", // Adjust positioning according to your Figma design
  },
  logoText: {
    position: "absolute",
    bottom: "10%", // Adjust positioning according to your Figma design
    alignSelf: "center",
    fontSize: 24, // Adjust the size according to your Figma design
    color: "#000000", // Use the specific color code for your text
    // Include any additional text styling from your Figma design
  },
});

export default Results;
