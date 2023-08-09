import 'package:flutter/material.dart';
import 'package:client/screens/login.dart';
import 'package:client/screens/tabs.dart';
import 'package:go_router/go_router.dart';

class AppRoutes {
  static const String login = '/';
  static const String tabs = '/tabs';
}

class AppRouter {
  static final GoRouter router = GoRouter(
    initialLocation: AppRoutes.login,
    navigatorKey: GlobalKey<NavigatorState>(),
    routes: [
      GoRoute(
        path: AppRoutes.login,
        builder: (context, state) => const LoginScreen(),
      ),
      GoRoute(
        path: AppRoutes.tabs,
        builder: (context, state) => const InventoryOverviewScreen(),
      ),
    ],
  );
  static GoRouter get instance => router;
}
