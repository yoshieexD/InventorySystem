import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:flutter_dotenv/flutter_dotenv.dart';

Future<String> fetchInventoryOverview() async {
  final response =
      await http.get(Uri.parse('${dotenv.env['API_URL']}/inventory_overview'));
  if (response.statusCode == 200) {
    return response.body;
  } else {
    throw Exception('Failed to load inventory overview');
  }
}

class InventoryOverviewScreen extends StatefulWidget {
  // Add a named constructor with the key parameter
  const InventoryOverviewScreen({Key? key}) : super(key: key);

  @override
  _InventoryOverviewScreenState createState() =>
      _InventoryOverviewScreenState();
}

class _InventoryOverviewScreenState extends State<InventoryOverviewScreen> {
  String _inventoryOverviewData = '';

  @override
  void initState() {
    super.initState();
    _loadInventoryOverview();
  }

  Future<void> _loadInventoryOverview() async {
    try {
      String data = await fetchInventoryOverview();
      setState(() {
        _inventoryOverviewData = data;
      });
    } catch (e) {
      setState(() {
        _inventoryOverviewData = 'Error: $e';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Inventory Overview'),
      ),
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Text(_inventoryOverviewData),
        ),
      ),
    );
  }
}
