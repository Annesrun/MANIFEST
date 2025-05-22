import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'package:tflite/tflite.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final cameras = await availableCameras();
  runApp(PedAnalyzer(camera: cameras.first));
}

class PedAnalyzer extends StatefulWidget {
  final CameraDescription camera;
  
  const PedAnalyzer({Key? key, required this.camera}) : super(key: key);

  @override
  _PedAnalyzerState createState() => _PedAnalyzerState();
}

class _PedAnalyzerState extends State<PedAnalyzer> {
  late CameraController _controller;
  late Future<void> _initializeControllerFuture;
  int _analyzedCount = 0;
  String _result = "";
  bool _isAnalyzing = false;

  @override
  void initState() {
    super.initState();
    _controller = CameraController(
      widget.camera,
      ResolutionPreset.medium,
    );
    _initializeControllerFuture = _controller.initialize();
    loadModel();
  }

  Future loadModel() async {
    await Tflite.loadModel(
      model: "assets/ped_model_resnet.tflite",
      labels: "assets/labels.txt",
    );
  }

  Future<void> analyzeImage() async {
    if (_isAnalyzing) return;
    
    setState(() {
      _isAnalyzing = true;
    });

    try {
      final image = await _controller.takePicture();
      
      var recognitions = await Tflite.runModelOnImage(
        path: image.path,
        numResults: 1,
        threshold: 0.5,
        imageMean: 127.5,
        imageStd: 127.5,
      );

      if (recognitions != null && recognitions.isNotEmpty) {
        setState(() {
          _analyzedCount++;
          _result = "Ped #$_analyzedCount\n${recognitions[0]["label"]}\n"
                   "Güven: ${(recognitions[0]["confidence"] * 100).toStringAsFixed(1)}%";
        });
      }
    } catch (e) {
      print(e);
    }

    setState(() {
      _isAnalyzing = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(title: Text('Ped Analiz')),
        body: FutureBuilder<void>(
          future: _initializeControllerFuture,
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.done) {
              return Column(
                children: [
                  Expanded(
                    child: Stack(
                      alignment: Alignment.center,
                      children: [
                        CameraPreview(_controller),
                        // Hedef çerçeve
                        CustomPaint(
                          painter: TargetPainter(),
                          child: Container(),
                        ),
                      ],
                    ),
                  ),
                  Container(
                    padding: EdgeInsets.all(16),
                    color: Colors.black87,
                    child: Column(
                      children: [
                        Text(
                          _result,
                          style: TextStyle(color: Colors.white, fontSize: 18),
                        ),
                        SizedBox(height: 10),
                        ElevatedButton(
                          onPressed: _isAnalyzing ? null : analyzeImage,
                          child: Text(_isAnalyzing ? 'Analiz ediliyor...' : 'Analiz Et'),
                        ),
                      ],
                    ),
                  ),
                ],
              );
            } else {
              return Center(child: CircularProgressIndicator());
            }
          },
        ),
      ),
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    Tflite.close();
    super.dispose();
  }
}

// Hedef çerçeve çizimi
class TargetPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = Colors.green
      ..style = PaintingStyle.stroke
      ..strokeWidth = 2.0;

    final rect = Rect.fromCenter(
      center: Offset(size.width / 2, size.height / 2),
      width: size.width * 0.7,
      height: size.width * 0.7,
    );

    canvas.drawRect(rect, paint);
  }

  @override
  bool shouldRepaint(CustomPainter oldDelegate) => false;
} 