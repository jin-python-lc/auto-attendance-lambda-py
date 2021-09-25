import React from 'react';
import { SafeAreaView, StyleSheet, StatusBar} from 'react-native';
import { WebView } from 'react-native-webview';

const App: React.FC = () => {
  return (
    <>
      <StatusBar barStyle="dark-content" />
      <SafeAreaView style={{flex: 1}}>
        <WebView source={{uri: "http://**************.s3-website-ap-northeast-1.amazonaws.com/"}} />
      </SafeAreaView>
    </>
  );
};

const styles = StyleSheet.create({});

export default App;