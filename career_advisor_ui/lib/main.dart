import 'package:flutter/material.dart';
import 'screens/login_screen.dart';
import 'screens/register_screen.dart';
import 'screens/quiz_screen.dart';
import 'screens/results_screen.dart';

void main() {
  runApp(const CareerAdvisorApp());
}

class CareerAdvisorApp extends StatelessWidget {
  const CareerAdvisorApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AI Career Advisor',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      initialRoute: '/',
      routes: {
        '/': (context) => LoginScreen(),
        '/register': (context) => RegisterScreen(),
        '/quiz': (context) => QuizScreen(),
        '/results': (context) => ResultsScreen(),
      },
    );
  }
}
