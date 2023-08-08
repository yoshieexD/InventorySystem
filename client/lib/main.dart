import 'package:flutter/material.dart';
import 'package:client/screens/tabs.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:client/screens/login.dart';

void main() async {
  await dotenv.load(fileName: '.env');
  runApp(const App());
}

class App extends StatelessWidget {
  const App({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: LoginScreen(),
    );
  }
}
