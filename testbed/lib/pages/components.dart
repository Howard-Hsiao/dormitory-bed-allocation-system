import 'dart:io';
import 'package:flutter/material.dart';
import '../conf/UI_conf.dart';

void alertSnackBar(GlobalKey<ScaffoldState> _scaffoldKey, String msg) {
  _scaffoldKey.currentState.showSnackBar(
    SnackBar(
      content: Row(children: [
        Icon(
          Icons.error_outline,
          color: Colors.black,
        ),
        SizedBox(
          width: 10.0,
        ),
        Text(
          msg,
          style: TextStyle(
            color: Colors.black,
            fontFamily: 'Noto_Sans_TC',
            fontWeight: FontWeight.w400,
            fontSize: 14.0,
          ),
        ),
      ]),
      backgroundColor: Colors.amber[300],
    ),
  );
}

Widget appBar() {
  return AppBar(
    title: Text(
      '臺大宿舍抽籤系統',
      style: TextStyle(
        fontSize: 28.0,
        color: Colors.white,
        fontFamily: 'Noto_Sans_TC',
        fontWeight: FontWeight.w500,
      ),
    ),
    centerTitle: false,
    backgroundColor: ui_col.main,
    elevation: 0.0,
  );
}
