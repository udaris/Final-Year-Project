/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 *
 * @format
 */

import React, { Component, useState } from 'react';
import {
    SafeAreaView,
    ScrollView,
    StatusBar,
    StyleSheet,
    // TextInput,
    TouchableOpacity,
    Image,
    Text,
    View,
} from 'react-native';
import { Button, TextInput } from 'react-native-paper';
import { launchImageLibrary } from 'react-native-image-picker';
import ImgToBase64 from 'react-native-image-base64';


function Create(props) {

    const [file, setfile] = useState(null);
    const [prediction, setPrediction] = useState('');
    const [imageUrl, setImageUrl] = useState('');
    const [loader, setLoader] = useState(false);

    const handleImageUpload = async (setfile) => {
        console.log("dd")
        if (!setfile|| !setfile.uri) return;

        setLoader(true);

        try {
            const base64String = await ImgToBase64.getBase64String(file.uri);

            const response = await fetch('http://192.168.8.197:3000/plant', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ file: base64String }),
            });

            if (!response.ok) {
                throw new Error('Failed to upload image');
            }

            const data = await response.json();
            setPrediction(data.prediction);
            setImageUrl(data.imageUrl);
        } catch (error) {
            console.error(error);
        } finally {
            setLoader(false);
        }
    };


    const openGallery = () => {
        launchImageLibrary('photo', (response) => {
            if (response.didCancel) {
                console.log('Image selection canceled');
            } else if (response.errorCode) {
                console.error('Image selection error:', response.errorMessage);
            } else {
                console.log("open err")
                setfile(response);
            }
        });
    };



    return (
        <View style={{ margin: 15, alignItems: 'center' }}>
            <View style={{ backgroundColor: 'yellow', alignItems: 'center', padding: 20 }}>
                <Text style={{ color: 'black', fontSize: 20, marginBottom: 10 }}>Ayurveda Plants Prediction</Text>
                <Text style={{ color: 'black', fontSize: 16, marginBottom: 20 }}>Upload an image and click submit</Text>

                <View style={{ marginBottom: 10 }}>
                    <View style={{ height: 160, justifyContent: 'center', alignItems: 'center' }}>
                        <TouchableOpacity onPress={openGallery} style={styles.imageButton}>
                            <Image
                                source={{
                                    uri: file ? file.uri 
                                                    : 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRtW8NV0SV4tox4P6StdN890M2ZMUkQ4_MLnrhMrB3J-wgjM6ZN-EhcF7JCS-9wKAAdyDM&usqp=CAU'
                                            }}
                                            style={styles.image}
                                        />
                        </TouchableOpacity>

                    </View>
                    <TouchableOpacity style={styles.submitButton} onPress={() => handleImageUpload(file)}>
                        <Text style={styles.submitButtonText}>Predict</Text>
                    </TouchableOpacity>
                </View>

                {prediction ? (
                    <View style={styles.predictionContainer}>
                        <Text style={styles.predictionText}>
                            Diagnosis for the following image is:
                        </Text>
                        <Text style={styles.predictionResult}>{prediction}</Text>
                        <Image source={{ uri: imageUrl }} style={styles.resultImage} />
                    </View>
                ) : <Text>not detrails</Text>}

                <Text>hh</Text>

            </View>


        </View>

    );
};

const styles = StyleSheet.create({
    input: {
        padding: 10,
        marginTop: 10,
        width: 200
    },
    image: {
        height: 90,
        width: 90,
        borderRadius: 45,
    },
    submitButton: {
        backgroundColor: 'white',
        marginTop: 20,
        paddingHorizontal: 20,
        paddingVertical: 10,
    },
    submitButtonText: {
        fontSize: 16,
        color: 'black',
    },
    predictionContainer: {
        marginTop: 20,
        alignItems: 'center',
    },
    predictionText: {
        color: 'black',
        fontSize: 16,
        marginBottom: 10,
    },
    predictionResult: {
        color: 'black',
        fontSize: 16,
        marginBottom: 20,
    },
    resultImage: {
        width: 300,
        height: 225,
    },
});

export default Create;
