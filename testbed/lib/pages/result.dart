import 'dart:io';
import 'package:flutter/material.dart';
import 'package:excel/excel.dart';

import 'package:file_chooser/file_chooser.dart';
import '../conf/dorm_conf.dart';
import '../conf/UI_conf.dart';
import './resultHelper/dataTab.dart';

class Result extends StatefulWidget {
  @override
  _ResultState createState() => _ResultState();
}

class _ResultState extends State<Result> with SingleTickerProviderStateMixin {
  // deal with tab
  TabController controller;
  Map dormData = new Map();

  @override
  void initState() {
    super.initState();
    controller = new TabController(vsync: this, length: 4);
  }

  @override
  void dispose() {
    controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    // extract q data
    final arguments = ModalRoute.of(context).settings.arguments as Map;
    final result = arguments['result'];

    for (int i = 0; i < dataName.length; i++) {
      dormData[dataName[i]] = DataTab(dataName[i], result[dataName[i]]);
    }
    // this.dormData = DormData(result);

    return Scaffold(
      backgroundColor: Colors.white,

      // app bar
      appBar: AppBar(
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
          actions: <Widget>[
            Container(
                padding: EdgeInsets.all(10),
                child: RaisedButton(
                  padding: EdgeInsets.all(0),
                  onPressed: () {
                    showSavePanel(suggestedFileName: '宿舍分配結果_總.xlsx')
                        .then((result) {
                      saveAllData(result.paths[0]);
                    });
                  },
                  child: Padding(
                    padding: EdgeInsets.all(5.0),
                    child: Text(
                      '匯出全部資料',
                      style: ui_text.general_b,
                    ),
                  ),
                  color: ui_col.exportButton,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(18.0),
                  ),
                ))
          ],
          bottom: new TabBar(controller: controller, tabs: <Tab>[
            new Tab(text: chi_boyDorm),
            new Tab(text: chi_girlDorm),
            new Tab(text: chi_bot_boy),
            new Tab(text: chi_bot_girl),
          ])),

      // body
      body: TabBarView(controller: controller, children: <Widget>[
        dormData[boyDorm],
        dormData[girlDorm],
        dormData[bot_boy],
        dormData[bot_girl]
      ]),
      // bottomNavigationBar: Text(jsonDecode(testing)),
    );
  }

  void saveAllData(storePath) {
    var excel = Excel.createExcel();
    dormData.forEach((dormName, dormTab) {
      dormTab.dormData.saveAllHelper(excel);
    });

    excel.delete("Sheet1");

    excel.encode().then((onValue) {
      File(storePath)
        ..createSync(recursive: true)
        ..writeAsBytesSync(onValue);
    });
  }
}
