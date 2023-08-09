import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'dart:convert';

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
  const InventoryOverviewScreen({Key? key}) : super(key: key);

  @override
  InventoryOverviewScreenState createState() => InventoryOverviewScreenState();
}

class InventoryOverviewScreenState extends State<InventoryOverviewScreen> {
  String _inventoryOverviewData = '';
  bool _isLoading = true;
  bool _hasError = false;

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
        _isLoading = false;
        _hasError = false;
      });
    } catch (e) {
      setState(() {
        _inventoryOverviewData = 'Error: $e';
        _isLoading = false;
        _hasError = true;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Inventory Overview'),
      ),
      body: _isLoading
          ? _buildLoadingIndicator()
          : _hasError
              ? _buildErrorWidget()
              : _buildInventoryOverview(),
    );
  }

  Widget _buildLoadingIndicator() {
    return const Center(
      child: CircularProgressIndicator(),
    );
  }

  Widget _buildErrorWidget() {
    return const Center(
      child: Text(
        'Error: Failed to load inventory overview',
        style: TextStyle(color: Colors.red),
      ),
    );
  }

  Widget _buildInventoryOverview() {
    final List<dynamic> inventoryData = json.decode(_inventoryOverviewData);

    return ListView.builder(
      itemCount: inventoryData.length,
      itemBuilder: (context, index) {
        final item = inventoryData[index];
        return Card(
          elevation: 3,
          margin: const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
          child: ListTile(
            title: Text(
              item['name'],
              style: const TextStyle(fontWeight: FontWeight.bold),
            ),
            subtitle: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const SizedBox(height: 8),
                Text("Code: ${item['code']}"),
                const SizedBox(height: 4),
                Text("Sequence: ${item['sequence']}"),
              ],
            ),
          ),
        );
      },
    );
  }
}
