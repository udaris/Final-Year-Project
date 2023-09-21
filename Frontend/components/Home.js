/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 *
 * @format
 */

import React, { useState, useEffect } from 'react';
import {
  FlatList,
  StyleSheet,
  Text,
  View, TouchableOpacity,
} from 'react-native';
import { Card, FAB } from 'react-native-paper';

function Home(props) {

  const [data, setData] = useState([])
  const [loading, setisloading] = useState(true)

  const loadData = () => {
    fetch('http://192.168.8.197:3000/get', {
      method: 'GET'
    })
      .then(resp => resp.json())
      .then(article => {
        setData(article)
        setisloading(false)
        console.log("success");
      }).catch((error) => {
        console.log("Api call error");
      });
  }

  useEffect(() => {
    loadData()
  }, [])

  const clickedItem = (data) => {
    props.navigation.navigate('Details', { data: data })
  }

  const renderData = (item) => {
    return (
      <Card style={styles.cardStyle}>
        <Text style={{ color: 'black' }} onPress={() => clickedItem(item)}>{item.title}</Text>
        <Text>{item.body}</Text>
      </Card>
    )
  }


  return (
    <View style={styles.container}>
      {/* <FlatList
        data={data}
        renderItem={({ item }) => {
          return renderData(item)
        }}
        onRefresh={() => loadData()}
        refreshing={loading}
        keyExtractor={item => '${item.id}'}
      /> */}
      <FAB
        style={styles.fab}
        small={false}

        theme={{ colors: { accent: "green" } }}
        onPress={() => props.navigation.navigate('Create')}
      />
      <TouchableOpacity onPress={()=>props.navigation.navigate('Module')}
        style={{ backgroundColor: "blue", width: 57, height: 30, margin: 10 }}><Text>Next</Text></TouchableOpacity>


    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1
  },
  cardStyle: {
    margin: 10,
    padding: 10
  },
  fab: {
    position: 'absolute',
    margin: 16,
    right: 0,
    bottom: 0
  }
});

export default Home;
