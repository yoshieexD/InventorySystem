import 'package:dio/dio.dart';
import 'package:go_router/go_router.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

class ApiProvider {
  final Dio dio = Dio();

  Future _get(String res) async {
    try {
      dio.options.extra['withCredentials'] = true;
      final response = await dio.get(
        "${dotenv.env['API_URL']}" "$res",
      );
      print(response);
      return response;
    } catch (error) {
      return error;
    }
  }

  Future _post(String res, [Map<String, dynamic>? data]) async {
    try {
      dio.options.extra['withCredentials'] = true;

      final response = await dio.post(
        "${dotenv.env['API_URL']}" "$res",
        data: data,
      );
      return response;
    } catch (err) {
      return err;
    }
  }

  void login(String email, String password, context) async {
    Response response = await _post(
      "/login",
      {
        'email': email,
        'password': password,
      },
    );

    if (response.statusCode == 200) {
      GoRouter.of(context).push("/");
    }
  }
}
