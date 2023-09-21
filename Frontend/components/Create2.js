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


function Create2(props) {
    const [title, setTitle] = useState("")
    const [body, setBody] = useState("")

    const insertData = () => {
        fetch('http://192.168.8.197:3000/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ title: title, body: body })
        })
            .then(resp => resp.json())
            .then(data => {
                props.navigation.navigate('Home')

            })
            .catch(error => console.log(error))
    }


    return (
        <View style={{ margin: 15, alignItems: 'center' }}>
            <Text>Create </Text>
            <TextInput style={styles.input}
                label="Title"
                value={title}
                mode='outlined'
                onChangeText={text => setTitle(text)}
            />
            <TextInput style={styles.input}
                label="Description"
                value={body}
                mode='outlined'
                numberOfLines={10}
                onChangeText={text => setBody(text)}
            />
            <Button
                style={{ marginTop: 15 }}
                title="Insert Article"
                mode='contained'
                onPress={() => insertData()}
            >Insert New</Button>
          
            
       {/* <TouchableOpacity style={{ height: 90, width: 90, borderRadius: 45 }} onPress={()=>openGallery()}>
                            <Image
                            source={{ uri: this.state.imageUrl === '' ? 'https://icons.iconarchive.com/icons/graphicloads/flat-finance/256/person-icon.png' : this.state.imageUrl }} style={{ height: 90, width: 90, borderRadius: 45 }} />
                        </TouchableOpacity> */}

        </View>

    );
};

const styles = StyleSheet.create({
    input: {
        padding: 10,
        marginTop: 10,
        width: 200
    }
});

export default Create2;
