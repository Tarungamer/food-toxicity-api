import 'package:flutter/material.dart';
import 'package:mobile_scanner/mobile_scanner.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(FoodToxicityApp());
}

class FoodToxicityApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: HomeScreen(),
    );
  }
}

class HomeScreen extends StatefulWidget {
  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  String? barcodeResult;
  Map<String, dynamic>? apiResult;
  bool isLoading = false;

  Future<void> fetchProductData(String barcode) async {
    setState(() {
      isLoading = true;
    });

    const String apiUrl = "https://food-toxicity-api.herokuapp.com/scan_barcode"; // Change to your API URL

    try {
      final response = await http.post(
        Uri.parse(apiUrl),
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({"barcode": barcode}),
      );

      if (response.statusCode == 200) {
        setState(() {
          apiResult = json.decode(response.body);
        });
      } else {
        setState(() {
          apiResult = {"error": "Product not found"};
        });
      }
    } catch (e) {
      setState(() {
        apiResult = {"error": "API request failed"};
      });
    } finally {
      setState(() {
        isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Food Toxicity Scanner")),
      body: Padding(
        padding: EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            Text(
              "Scan a Barcode",
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            SizedBox(height: 20),
            Container(
              height: 300,
              width: double.infinity,
              decoration: BoxDecoration(border: Border.all(color: Colors.blueAccent)),
              child: MobileScanner(
                onDetect: (capture) {
                  final List<Barcode> barcodes = capture.barcodes;
                  if (barcodes.isNotEmpty && barcodes.first.rawValue != null) {
                    setState(() {
                      barcodeResult = barcodes.first.rawValue!;
                    });
                    fetchProductData(barcodes.first.rawValue!);
                  }
                },
              ),
            ),
            SizedBox(height: 20),
            barcodeResult != null
                ? Text("Scanned Barcode: $barcodeResult", style: TextStyle(fontSize: 16))
                : Text("No barcode scanned yet."),
            SizedBox(height: 20),
            isLoading
                ? CircularProgressIndicator()
                : apiResult != null
                    ? Expanded(
                        child: SingleChildScrollView(
                          child: Column(
                            children: [
                              Text(
                                "Product Name: ${apiResult!['product_name'] ?? 'Unknown'}",
                                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                              ),
                              SizedBox(height: 10),
                              apiResult!["image_url"] != null
                                  ? Image.network(apiResult!["image_url"], height: 150)
                                  : Text("No Image Available"),
                              SizedBox(height: 10),
                              Text("Energy (kcal): ${apiResult!['energy-kcal_100g'] ?? 'N/A'}"),
                              Text("NOVA Group: ${apiResult!['nova_group'] ?? 'N/A'}"),
                              Text("Number of Additives: ${apiResult!['additives_n'] ?? 'N/A'}"),
                            ],
                          ),
                        ),
                      )
                    : Container(),
          ],
        ),
      ),
    );
  }
}
