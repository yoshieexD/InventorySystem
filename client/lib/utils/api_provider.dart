import 'package:http/http.dart' as http;
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'dart:convert';

class ApiService {
  static Future<bool> loginUser(String username, String password) async {
    final response = await http.post(
      Uri.parse('${dotenv.env['API_URL']}/login2'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'username': username, 'password': password}),
    );

    if (response.statusCode == 200) {
      final responseBody = response.body;
      if (responseBody.contains('Logged in')) {
        return true;
      }
    }
    return false;
  }
}
