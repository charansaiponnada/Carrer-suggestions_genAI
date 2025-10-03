import 'package:flutter/material.dart';
import 'package:career_advisor_ui/services/api_service.dart';
// We will import our ApiService later when we add the logic

class LoginScreen extends StatefulWidget {
  // StatefulWidget is used because the screen's content will change
  // (e.g., showing a loading indicator or an error message).
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  // TextEditingControllers are used to read the text from the input fields.
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();

  // This will be used to show a loading circle while we talk to the backend.
  bool _isLoading = false;

  // This will hold any error messages from the backend.
  String? _errorMessage;

  // --- LOGIN LOGIC ---
  Future<void> _login() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    final email = _emailController.text;
    final password = _passwordController.text;

    if (email.isEmpty || password.isEmpty) {
      setState(() {
        _errorMessage = "Please enter both email and password.";
        _isLoading = false;
      });
      return;
    }

    // Call the ApiService to login the user.
    final result = await ApiService.loginUser(email, password);

    if (result.containsKey('message')) {
      // SUCCESS! The user was logged in.
      final String uid = result['uid'];
      if (mounted) {
        Navigator.pushReplacementNamed(context, '/quiz', arguments: uid);
      }
    } else if (result.containsKey('detail')) {
      setState(() {
        _errorMessage = result['detail'];
      });
    } else {
      setState(() {
        _errorMessage = 'An unknown error occurred.';
      });
    }

    setState(() {
      _isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('AI Career Advisor Login')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            TextField(
              controller: _emailController,
              keyboardType: TextInputType.emailAddress,
              decoration: const InputDecoration(
                labelText: 'Email',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 16),
            TextField(
              controller: _passwordController,
              obscureText: true,
              decoration: const InputDecoration(
                labelText: 'Password',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 24),
            _isLoading
                ? const Center(child: CircularProgressIndicator())
                : ElevatedButton(
                    onPressed: _login,
                    style: ElevatedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(vertical: 16),
                    ),
                    child: const Text('Login'),
                  ),
            // Register navigation
            TextButton(
              onPressed: () {
                Navigator.pushNamed(context, '/register');
              },
              child: const Text("Don't have an account? Register here"),
            ),
            if (_errorMessage != null)
              Padding(
                padding: const EdgeInsets.only(top: 16),
                child: Text(
                  _errorMessage!,
                  style: const TextStyle(color: Colors.red),
                  textAlign: TextAlign.center,
                ),
              ),
          ],
        ),
      ),
    );
  }
}
