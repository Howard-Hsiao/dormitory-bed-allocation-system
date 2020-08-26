import 'dart:io';
import 'dart:convert';
import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import 'package:file_chooser/file_chooser.dart';

import 'package:excel/excel.dart';
import 'package:http/http.dart' as http;
import 'package:dio/dio.dart';

import 'components.dart';
import '../conf/UI_conf.dart';

/// Given a relative path, extract its file name and truncate it into a displayable length (maxLen) if required.
String truncateToDisplay(String path) {
  if (path == '尚未選擇檔案') return path;

  var result = path.split('/').last;
  const maxLen = 25;
  if (result.length > maxLen) {
    result = result.substring(0, maxLen - 4);
    result += '...';
  }
  return result;
}

class Home extends StatefulWidget {
  @override
  _HomeState createState() => _HomeState();
}

class _HomeState extends State<Home> {
  final _scaffoldKey = GlobalKey<ScaffoldState>();
  String studentDataPath = '尚未選擇檔案';
  String bedDataPath = '尚未選擇檔案';
  List studentData = [];
  List bedData = [];
  bool isProcessing = false;

  Future getIdentityPool() async {
    const url = 'http://127.0.0.1:5000/api/get_all_identities/';
    final body = jsonEncode(studentData);

    var response;
    while (true) {
      try {
        response = await http.post(
          url,
          headers: {HttpHeaders.contentTypeHeader: 'application/json'},
          body: body,
        );
        break;
      } on SocketException {}
    }
    // dio
    // Dio dio = new Dio();
    // final response = await dio.post(
    //   url,
    //   options: Options(sendTimeout: 5000, receiveTimeout: 30000),
    //   data: body,
    // );

    return response;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      key: _scaffoldKey,
      backgroundColor: Colors.white,

      // app bar
      appBar: appBar(),

      // body
      body: Container(
        margin: EdgeInsets.symmetric(vertical: 30.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: <Widget>[
            // title
            Expanded(
              flex: 2,
              child: Container(
                padding: EdgeInsets.symmetric(horizontal: 120.0),
                child: Align(
                  alignment: Alignment.centerLeft,
                  child: Text(
                    '[ 步驟一 ] 匯入資料',
                    style: TextStyle(
                      color: Colors.black,
                      fontFamily: 'Noto_Sans_TC',
                      fontWeight: FontWeight.w700,
                      fontSize: 24.0,
                    ),
                  ),
                ),
              ),
            ),

            // two main panels
            Expanded(
              flex: 10,
              child: Container(
                padding: EdgeInsets.symmetric(vertical: 0.0, horizontal: 120.0),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: <Widget>[
                    Divider(
                      height: 5.0,
                      thickness: 3.0,
                      color: Colors.grey[300],
                    ),

                    // up panel
                    Expanded(
                      child: Container(
                        color: Colors.white,
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: <Widget>[
                            Text(
                              '匯入學生資料',
                              style: TextStyle(
                                color: Colors.black,
                                fontFamily: 'Noto_Sans_TC',
                                fontWeight: FontWeight.w300,
                                fontSize: 24.0,
                              ),
                            ),
                            Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              crossAxisAlignment: CrossAxisAlignment.center,
                              children: <Widget>[
                                Text(
                                  '${truncateToDisplay(studentDataPath)}',
                                  style: TextStyle(
                                    color: Colors.grey,
                                    fontFamily: 'Noto_Sans_TC',
                                    fontWeight: FontWeight.w300,
                                    fontSize: 14.0,
                                  ),
                                ),
                                FlatButton(
                                  onPressed: () async {
                                    final result = await showOpenPanel(
                                        allowsMultipleSelection: false,
                                        allowedFileTypes: <FileTypeFilterGroup>[
                                          FileTypeFilterGroup(
                                              fileExtensions: <String>[
                                                'xlsx',
                                                'xls'
                                              ])
                                        ]);
                                    setState(() {
                                      if (result.paths.isNotEmpty) {
                                        studentDataPath = result.paths[0];
                                      }
                                    });
                                  },
                                  child: Text(
                                    '選擇檔案',
                                    style: ui_text.general_w,
                                  ),
                                  color: ui_col.main,
                                  shape: RoundedRectangleBorder(
                                    borderRadius: BorderRadius.circular(18.0),
                                  ),
                                ),
                              ],
                            ),
                          ],
                        ),
                      ),
                    ),

                    Divider(
                      height: 5.0,
                      thickness: 1.0,
                      color: Colors.grey[300],
                    ),

                    // down panel
                    Expanded(
                      child: Container(
                        color: Colors.white,
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: <Widget>[
                            Text(
                              '匯入床位資料',
                              style: TextStyle(
                                color: Colors.black,
                                fontFamily: 'Noto_Sans_TC',
                                fontWeight: FontWeight.w300,
                                fontSize: 24.0,
                              ),
                            ),
                            Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              crossAxisAlignment: CrossAxisAlignment.center,
                              children: <Widget>[
                                Text(
                                  '${truncateToDisplay(bedDataPath)}',
                                  style: TextStyle(
                                    color: Colors.grey,
                                    fontFamily: 'Noto_Sans_TC',
                                    fontWeight: FontWeight.w300,
                                    fontSize: 14.0,
                                  ),
                                ),
                                FlatButton(
                                  onPressed: () async {
                                    final result = await showOpenPanel(
                                        allowsMultipleSelection: false,
                                        allowedFileTypes: <FileTypeFilterGroup>[
                                          FileTypeFilterGroup(
                                              fileExtensions: <String>[
                                                'xlsx',
                                                'xls'
                                              ])
                                        ]);
                                    if (result.paths.isNotEmpty) {
                                      setState(() {
                                        bedDataPath = result.paths[0];
                                      });
                                    }
                                  },
                                  child: Text(
                                    '選擇檔案',
                                    style: ui_text.general_w,
                                  ),
                                  color: ui_col.main,
                                  shape: RoundedRectangleBorder(
                                    borderRadius: BorderRadius.circular(18.0),
                                  ),
                                ),
                              ],
                            ),
                          ],
                        ),
                      ),
                    ),

                    Divider(
                      height: 5.0,
                      thickness: 3.0,
                      color: Colors.grey[300],
                    ),
                  ],
                ),
              ),
            ),

            // done button
            Expanded(
              flex: 2,
              child: Container(
                padding:
                    EdgeInsets.symmetric(vertical: 15.0, horizontal: 120.0),
                child: FlatButton(
                  color: isProcessing ? Colors.indigo[900] : Colors.indigo,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(50.0),
                  ),
                  onPressed: () async {
                    // file not selected
                    if (studentDataPath == '尚未選擇檔案' ||
                        bedDataPath == '尚未選擇檔案') {
                      alertSnackBar(_scaffoldKey, '請選擇檔案');
                    }
                    // read data, get identity pool, navigate
                    else {
                      setState(() {
                        isProcessing = true;
                      });
                      await Future.delayed(const Duration(milliseconds: 100));

                      // extract student data
                      var bytes = File(studentDataPath).readAsBytesSync();
                      var excel = Excel.decodeBytes(bytes);
                      if (excel.tables.keys.length == 1) {
                        for (var table in excel.tables.keys) {
                          studentData = excel.tables[table].rows;
                          // print(studentData[0]);
                        }
                      } else {
                        alertSnackBar(_scaffoldKey, '學生資料表有多張工作表，請更正後重新匯入');
                      }

                      // extract bed data
                      bytes = File(bedDataPath).readAsBytesSync();
                      excel = Excel.decodeBytes(bytes);
                      if (excel.tables.keys.length == 1) {
                        for (var table in excel.tables.keys) {
                          bedData = excel.tables[table].rows;
                          // print(bedData[0]);
                        }
                      } else {
                        alertSnackBar(_scaffoldKey, '床位資料表有多張工作表，請更正後重新匯入');
                      }

                      // get identity pool
                      List<String> identityPool;
                      await getIdentityPool().then((response) {
                        if (response.statusCode == 200) {
                          // identityPool = response.data.cast<String>();
                          identityPool =
                              jsonDecode(response.body).cast<String>();
                          // print(identityPool);
                        } else {
                          // TODO: deal with invalid response

                        }
                      });

                      setState(() {
                        isProcessing = false;
                      });

                      // Navigator.pushReplacementNamed(context, '/priority');
                      if (studentData.isNotEmpty && bedData.isNotEmpty) {
                        await Navigator.pushNamed(context, '/priority',
                            arguments: {
                              'studentData': studentData,
                              'bedData': bedData,
                              'identityPool': identityPool,
                            });
                      }
                    }
                  },
                  child: Text(
                    isProcessing ? '資料處理中' : '完成',
                    style: TextStyle(
                      color: Colors.white,
                      fontFamily: 'Noto_Sans_TC',
                      fontWeight: FontWeight.w100,
                      fontSize: 14.0,
                    ),
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
