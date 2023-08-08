import 'package:client/screens/tabs.dart';
import 'package:client/screens/login.dart';
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class AppRouter {
  static GoRouter returnRouter(bool isAuth) {
    GoRouter router = GoRouter(
      routes: [
        GoRoute(
          name: "login",
          path: '/login',
          pageBuilder: (context, state) {
            return const MaterialPage(child: LoginScreen());
          },
        ),
        GoRoute(
          name: "tabs",
          path: '/',
          pageBuilder: (context, state) {
            return const MaterialPage(child: InventoryOverviewScreen());
          },
        ),
      ],
    );
    return router;
  }
}
