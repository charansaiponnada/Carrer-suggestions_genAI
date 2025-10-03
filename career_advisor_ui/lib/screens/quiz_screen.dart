import 'package:flutter/material.dart';
import 'package:career_advisor_ui/services/api_service.dart';

class QuizScreen extends StatefulWidget {
  const QuizScreen({super.key});

  @override
  State<QuizScreen> createState() => _QuizScreenState();
}

class _QuizScreenState extends State<QuizScreen> {
  // Variables to hold the selected answers
  String? _problemSolvingStyle;
  String? _teamRole;
  String? _primaryInterest;
  String? _learningStyle;

  bool _isLoading = false;

  // This function will be called when the submit button is pressed.
  Future<void> _submitQuiz() async {
    // Get the UID that was passed from the LoginScreen
    final uid = ModalRoute.of(context)!.settings.arguments as String;

    // Basic validation
    if (_problemSolvingStyle == null ||
        _teamRole == null ||
        _primaryInterest == null ||
        _learningStyle == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Please answer all questions.')),
      );
      return;
    }

    setState(() {
      _isLoading = true;
    });

    final answers = {
      "uid": uid,
      "problem_solving_style": _problemSolvingStyle!,
      "team_role": _teamRole!,
      "primary_interest": _primaryInterest!,
      "learning_style": _learningStyle!,
    };

    // Call the API to submit the quiz
    final result = await ApiService.submitQuiz(answers);

    if (mounted) {
      if (result.containsKey('message')) {
        // Success! Now navigate to the results screen, passing the UID again.
        Navigator.pushReplacementNamed(context, '/results', arguments: uid);
      } else {
        // Show an error
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(result['detail'] ?? 'An error occurred.')),
        );
      }
    }

    setState(() {
      _isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Career Fingerprint Quiz')),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : SingleChildScrollView(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  _buildDropdown(
                    'Problem-Solving Style',
                    [
                      'Logical puzzles',
                      'Creative brainstorming',
                      'Hands-on building',
                    ],
                    _problemSolvingStyle,
                    (value) => setState(() => _problemSolvingStyle = value),
                  ),
                  _buildDropdown(
                    'Team Role',
                    [
                      'The leader',
                      'The planner',
                      'The creative idea person',
                      'The detail-oriented finisher',
                    ],
                    _teamRole,
                    (value) => setState(() => _teamRole = value),
                  ),
                  _buildDropdown(
                    'Primary Interest',
                    [
                      'Technology and AI',
                      'Arts and Design',
                      'Business and Finance',
                      'Healthcare and Biology',
                    ],
                    _primaryInterest,
                    (value) => setState(() => _primaryInterest = value),
                  ),
                  _buildDropdown(
                    'Learning Style',
                    [
                      'Reading books and articles',
                      'Watching video tutorials',
                      'Doing hands-on projects',
                    ],
                    _learningStyle,
                    (value) => setState(() => _learningStyle = value),
                  ),
                  const SizedBox(height: 32),
                  ElevatedButton(
                    onPressed: _submitQuiz,
                    style: ElevatedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(vertical: 16),
                    ),
                    child: const Text('Submit & Get Recommendation'),
                  ),
                ],
              ),
            ),
    );
  }

  // Helper widget to avoid repeating code for dropdowns
  Widget _buildDropdown(
    String title,
    List<String> items,
    String? currentValue,
    ValueChanged<String?> onChanged,
  ) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          title,
          style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
        ),
        const SizedBox(height: 8),
        DropdownButtonFormField<String>(
          initialValue: currentValue,
          items: items.map((String value) {
            return DropdownMenuItem<String>(value: value, child: Text(value));
          }).toList(),
          onChanged: onChanged,
          decoration: const InputDecoration(border: OutlineInputBorder()),
          isExpanded: true,
        ),
        const SizedBox(height: 24),
      ],
    );
  }
}
