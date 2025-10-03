import 'package:flutter/material.dart';
import 'package:career_advisor_ui/services/api_service.dart';

class ResultsScreen extends StatefulWidget {
  const ResultsScreen({super.key});

  @override
  State<ResultsScreen> createState() => _ResultsScreenState();
}

class _ResultsScreenState extends State<ResultsScreen> {
  Future<Map<String, dynamic>>? _recommendationFuture;

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    // We fetch the data here because it has access to the 'context'
    // needed to get the arguments from the previous screen.
    if (_recommendationFuture == null) {
      final uid = ModalRoute.of(context)!.settings.arguments as String;
      setState(() {
        _recommendationFuture = ApiService.getRecommendation(uid);
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Your AI-Generated Roadmap')),
      // FutureBuilder is a perfect widget for handling asynchronous data.
      // It automatically shows a loading indicator, an error message, or the data.
      body: FutureBuilder<Map<String, dynamic>>(
        future: _recommendationFuture,
        builder: (context, snapshot) {
          // 1. While waiting for data
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          // 2. If there was an error
          if (snapshot.hasError ||
              !snapshot.hasData ||
              snapshot.data!.containsKey('detail')) {
            return Center(
              child: Text(
                'Error: ${snapshot.data?['detail'] ?? snapshot.error.toString()}',
                style: const TextStyle(color: Colors.red),
                textAlign: TextAlign.center,
              ),
            );
          }
          // 3. If data is successfully loaded
          final data = snapshot.data!;
          final careers = data['recommended_careers'] as List;
          final skills = data['essential_skills'] as List;
          final roadmap = data['learning_roadmap'] as List;

          return ListView(
            padding: const EdgeInsets.all(16.0),
            children: [
              _buildSectionTitle('Top Career Recommendations'),
              ...careers.map(
                (career) => Card(
                  child: ListTile(
                    title: Text(
                      career['career'],
                      style: const TextStyle(fontWeight: FontWeight.bold),
                    ),
                    subtitle: Text(career['reason']),
                  ),
                ),
              ),
              const SizedBox(height: 24),

              _buildSectionTitle('Essential Skills to Develop'),
              ...skills.map((skill) => Chip(label: Text(skill.toString()))),
              const SizedBox(height: 24),

              _buildSectionTitle('Your First Steps'),
              ...roadmap.map(
                (step) => ListTile(
                  leading: const Icon(
                    Icons.check_circle_outline,
                    color: Colors.green,
                  ),
                  title: Text(step.toString()),
                ),
              ),
            ],
          );
        },
      ),
    );
  }

  Widget _buildSectionTitle(String title) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12.0),
      child: Text(
        title,
        style: const TextStyle(
          fontSize: 22,
          fontWeight: FontWeight.bold,
          color: Colors.blue,
        ),
      ),
    );
  }
}
