/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 *
 * @format
 */

import React, { Component } from 'react';
import {
  SafeAreaView,
  ScrollView,
  StatusBar,
  StyleSheet,
  Text,
  View,
} from 'react-native';

class ClassHome extends Component {
    render(){
        return(
            <View style={styles.container}>
              <Text>Class Home </Text>
              <Text>{this.props.name}</Text>
            </View>
          );
    }

};

const styles = StyleSheet.create({
  container: {
    marginTop: 32,
    alignItems:'center',
    justifyContent:'center'
  },
});

export default ClassHome;
