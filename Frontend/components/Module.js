import React, { useState } from 'react';
import { View, TouchableOpacity, Button, Image, StyleSheet, Text, Alert } from 'react-native';
import { launchImageLibrary } from 'react-native-image-picker';
import ImagePicker from 'react-native-image-picker';

const Module = () => {
  const [selectedImage, setSelectedImage] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [plantDetails, setPlantDetails] = useState(null);

  // Function to handle image selection
  const selectImage = () => {
    launchImageLibrary(
      {
        mediaType: 'photo',
      },
      response => {
        console.log(response); 
        if (!response.didCancel) {
          console.log(selectedImage); 
          setSelectedImage(response);
        }
      }
    );
  };

  // Function to send the selected image to the backend
  const uploadImage = async () => {
    if (!selectedImage) {
      Alert.alert('No image selected');
      return;
    }

    const formData = new FormData();
    formData.append('file', {
      uri: selectedImage.uri,
      type: selectedImage.type,
      name: selectedImage.fileName || 'image.jpg',
    });
    console.log("pee")
    try {
      const response = await fetch('http://192.168.8.197:3000/plant', {
        method: 'POST',
        body: formData,
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      const data = await response.json();

      if (response.ok) {
        setPrediction(data.predicted_class);
        setPlantDetails(data.plant_details);
      } else {
        Alert.alert('Error', data.error);
      }
    } catch (error) {
      Alert.alert('Error', error.message);
    }
  };

  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
      {selectedImage && selectedImage.uri && (
        <Image source={{ uri: selectedImage.uri }} style={{ width: 200, height: 200, marginBottom: 20 }} />
      )}

      <Button title="Select Image" onPress={selectImage} />

      <Button title="Upload Image" onPress={uploadImage} />


      {prediction && (
        <View>
          <Text>Predicted class: {prediction}</Text>
          {plantDetails && (
            <View>
              <Text>Plant details:</Text>
              <Text>Used for: {plantDetails.UsedFor}</Text>
              <Text>Plant part used: {plantDetails.PlantPartUsed}</Text>
              {/* Add any other plant details you want to display */}
            </View>
          )}
        </View>
      )}
    </View>
  );
};
const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  imageButton: {
    height: 200,
    width: 200,
    borderWidth: 1,
    borderColor: 'gray',
    borderRadius: 10,
    justifyContent: 'center',
    alignItems: 'center',
  },
  image: {
    height: 180,
    width: 180,
    borderRadius: 10,
  },
  placeholderText: {
    fontSize: 16,
    color: 'gray',
  },
});

export default Module;
