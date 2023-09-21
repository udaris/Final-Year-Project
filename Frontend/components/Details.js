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
    Text,
    View,
} from 'react-native';
import { Button, TextInput } from 'react-native-paper';

function Details(props) {
    const data=props.route.params.data;
    
    const [title, setTitle] = useState(data.title)
    const [body, setBody] = useState(data.body)

    const updateData = () => {
        fetch(`http://192.168.8.197:3000/update/${data.id}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ title: title, body: body })
        })
            .then(resp => resp.json())
            .then(data => {
                props.navigation.navigate('Home',{data:data})

            })
            .catch(error => console.log(error))
    }
    const deleteData = (data) => {
        fetch(`http://192.168.8.197:3000/delete/${data.id}/`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ title: title, body: body })
        })
            .then(resp => resp.json())
            .then(data => {
                props.navigation.navigate('Home',{data:data})

            })
            .catch(error => console.log(error))
    }

    return (
        <View style={{ margin: 15, alignItems: 'center' }}>
            <Text> </Text>
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
                style={{ margin: 15 }}
                title="Insert Article"
                mode='contained'
                onPress={() => updateData()}
            >Update Now</Button>
             <Button
                style={{ margin: 15 }}
                title="Insert Article"
                mode='contained'
                onPress={() => deleteData(data)}
            >Delete Now</Button>
            <Text></Text>
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

export default Details;
