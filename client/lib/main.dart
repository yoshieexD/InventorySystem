import 'package:flutter/material.dart';
import 'package:client/screens/login.dart';

void main() {
  runApp(const App());
}

class App extends StatelessWidget {
  const App({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(home: LoginScreen());
  }
}
