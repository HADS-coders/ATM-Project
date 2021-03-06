import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:splashscreen/splashscreen.dart';
import 'lockscreen.dart';
import 'home.dart';
import 'strings.dart';

class Splash extends StatefulWidget {
  @override
  _SplashState createState() => _SplashState();
}

class _SplashState extends State<Splash> {
  bool isLocked;
  String pin;
  void initState() {
    super.initState();
    getData();
    if (this.isLocked == null) {
      isLocked = false;
    }
  }

  Future<void> getData() async {
    SharedPreferences pref = await SharedPreferences.getInstance();
    bool isLocked =
        pref.getBool('isLocked') == null ? false : pref.getBool('isLocked');
    String pin = pref.getString('pin') ?? '';
    this.pin = pin;
    this.isLocked = isLocked;
    setState(() {});
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: SplashScreen(
        seconds: 1,
        navigateAfterSeconds: nextcreen(),
        title: Text(Strings.appBarTitle),
      ),
    );
  }

  Widget nextcreen() {
    return isLocked
        ? LockScreen(isLocked: this.isLocked, pin: this.pin)
        : Home(
            isLocked: this.isLocked,
            pin: this.pin,
          );
  }
}
