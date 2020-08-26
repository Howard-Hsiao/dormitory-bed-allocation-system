// import 'dart:js';
import 'dart:io';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:dio/dio.dart';

import 'components.dart';

/// Flatten: convert type 'list of list of strings' into type 'list of strings'
List<String> flatten(List<List<String>> li) {
  return li.expand((i) => i).toList();
}

class Priority extends StatefulWidget {
  @override
  _PriorityState createState() => _PriorityState();
}

class _PriorityState extends State<Priority> {
  List<String> identityPool;
  List<List<String>> identitySelected = [];
  bool isProcessing = false;

  Future getMatchResult(List studentData, List bedData) async {
    const url = 'http://127.0.0.1:5000/api/match/';
    final body = {
      'priority': identitySelected,
      'student': studentData,
      'beds': bedData,
    };

    var response;
    while (true) {
      try {
        response = await http.post(
          url,
          headers: {HttpHeaders.contentTypeHeader: 'application/json'},
          body: jsonEncode(body),
        );
        break;
      } on SocketException {}
    }

    // Dio dio = new Dio();
    // final response = await dio.post(
    //   url,
    //   options: Options(sendTimeout: 5000, receiveTimeout: 300000),
    //   data: body,
    // );

    return response;
  }

  @override
  Widget build(BuildContext context) {
    // extract data
    final arguments = ModalRoute.of(context).settings.arguments as Map;
    final studentData = arguments['studentData'];
    final bedData = arguments['bedData'];
    identityPool = arguments['identityPool'];

    return Scaffold(
      backgroundColor: Colors.white,

      // app bar
      appBar: appBar(),

      // body
      body: Container(
        margin: EdgeInsets.symmetric(vertical: 30.0),
        padding: EdgeInsets.symmetric(horizontal: 120.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: <Widget>[
            // title
            Expanded(
              flex: 2,
              child: Container(
                child: Align(
                  alignment: Alignment.centerLeft,
                  child: Text(
                    '[ 步驟二 ] 選擇身份別優先序',
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

            // identity selector
            Expanded(
                flex: 10,
                child: Container(
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      // identity pool
                      Expanded(
                        flex: 8,
                        child: Container(
                          color: Colors.grey[300],
                          child: ListView.builder(
                            itemCount: identityPool.length,
                            itemBuilder: (context, index) {
                              return Card(
                                child: ListTile(
                                    title: Text(
                                      identityPool[index],
                                      style: TextStyle(
                                        color: Colors.black,
                                        fontFamily: 'Noto_Sans_TC',
                                        fontWeight: FontWeight.w500,
                                        fontSize: 15.0,
                                      ),
                                    ),
                                    trailing: IconButton(
                                      icon: Icon(Icons.add),
                                      iconSize: 16.0,
                                      color: flatten(identitySelected)
                                              .contains(identityPool[index])
                                          ? Colors.grey[300]
                                          : Colors.grey[600],
                                      splashColor: Colors.transparent,
                                      highlightColor: Colors.transparent,
                                      tooltip: flatten(identitySelected)
                                              .contains(identityPool[index])
                                          ? null
                                          : '新增',
                                      hoverColor: Colors.transparent,
                                      onPressed: () {
                                        if (flatten(identitySelected).contains(
                                                identityPool[index]) ==
                                            false) {
                                          setState(() {
                                            identitySelected
                                                .add([identityPool[index]]);
                                          });
                                        }
                                      },
                                    )),
                              );
                            },
                          ),
                        ),
                      ),

                      Expanded(
                        flex: 1,
                        child: SizedBox(),
                      ),

                      // selected and ordered identities
                      Expanded(
                        flex: 8,
                        child: Container(
                          color: Colors.grey[300],
                          child: ListView.builder(
                            itemCount: identitySelected.length,
                            itemBuilder: (contextLevel1, indexLevel1) {
                              return Card(
                                child: ListTile(
                                  title: Row(
                                    mainAxisAlignment:
                                        MainAxisAlignment.spaceAround,
                                    crossAxisAlignment:
                                        CrossAxisAlignment.center,
                                    children: [
                                      // leading index
                                      Flexible(
                                        flex: 1,
                                        child: Text(
                                          '${indexLevel1 + 1}',
                                          style: TextStyle(
                                            color: Colors.grey[600],
                                            fontFamily: 'Noto_Sans_TC',
                                            fontWeight: FontWeight.w500,
                                            fontSize: 16.0,
                                          ),
                                        ),
                                      ),
                                      // card sets in one priority
                                      Flexible(
                                        flex: 5,
                                        child: ListView.builder(
                                            itemCount:
                                                identitySelected[indexLevel1]
                                                    .length,
                                            shrinkWrap: true,
                                            itemBuilder:
                                                (contextLevel2, indexLevel2) {
                                              return Card(
                                                child: ListTile(
                                                  title: Text(
                                                    identitySelected[
                                                            indexLevel1]
                                                        [indexLevel2],
                                                    style: TextStyle(
                                                      color: Colors.black,
                                                      fontFamily:
                                                          'Noto_Sans_TC',
                                                      fontWeight:
                                                          FontWeight.w500,
                                                      fontSize: 15.0,
                                                    ),
                                                  ),
                                                  trailing: Wrap(
                                                    spacing: -15,
                                                    children: [
                                                      IconButton(
                                                        icon: Icon(
                                                            Icons.arrow_upward),
                                                        iconSize: 14.0,
                                                        color: (indexLevel1 ==
                                                                    0 &&
                                                                identitySelected[
                                                                            indexLevel1]
                                                                        .length ==
                                                                    1)
                                                            ? Colors.grey[300]
                                                            : Colors.grey[600],
                                                        splashColor:
                                                            Colors.transparent,
                                                        highlightColor:
                                                            Colors.transparent,
                                                        tooltip: (indexLevel1 ==
                                                                    0 &&
                                                                identitySelected[
                                                                            indexLevel1]
                                                                        .length ==
                                                                    1)
                                                            ? null
                                                            : '上移一層',
                                                        hoverColor:
                                                            Colors.transparent,
                                                        onPressed: () {
                                                          setState(() {
                                                            // the only identity in this priority
                                                            if (indexLevel1 !=
                                                                    0 &&
                                                                identitySelected[
                                                                            indexLevel1]
                                                                        .length ==
                                                                    1) {
                                                              identitySelected[
                                                                      indexLevel1 -
                                                                          1] +=
                                                                  identitySelected[
                                                                      indexLevel1];
                                                              identitySelected
                                                                  .removeAt(
                                                                      indexLevel1);
                                                            }
                                                            // multiple identities in this priority
                                                            else if (identitySelected[
                                                                        indexLevel1]
                                                                    .length >
                                                                1) {
                                                              final toMove =
                                                                  identitySelected[
                                                                          indexLevel1]
                                                                      .removeAt(
                                                                          indexLevel2);
                                                              identitySelected
                                                                  .insert(
                                                                      indexLevel1,
                                                                      [toMove]);
                                                            }
                                                          });
                                                        },
                                                      ),
                                                      IconButton(
                                                        icon: Icon(Icons
                                                            .arrow_downward),
                                                        iconSize: 14.0,
                                                        color: (indexLevel1 ==
                                                                    identitySelected
                                                                            .length -
                                                                        1 &&
                                                                identitySelected[
                                                                            indexLevel1]
                                                                        .length ==
                                                                    1)
                                                            ? Colors.grey[300]
                                                            : Colors.grey[600],
                                                        splashColor:
                                                            Colors.transparent,
                                                        highlightColor:
                                                            Colors.transparent,
                                                        tooltip: (indexLevel1 ==
                                                                    identitySelected
                                                                            .length -
                                                                        1 &&
                                                                identitySelected[
                                                                            indexLevel1]
                                                                        .length ==
                                                                    1)
                                                            ? null
                                                            : '下移一層',
                                                        hoverColor:
                                                            Colors.transparent,
                                                        onPressed: () {
                                                          setState(() {
                                                            // the only identity in this priority
                                                            if (indexLevel1 !=
                                                                    identitySelected
                                                                            .length -
                                                                        1 &&
                                                                identitySelected[
                                                                            indexLevel1]
                                                                        .length ==
                                                                    1) {
                                                              identitySelected[
                                                                      indexLevel1 +
                                                                          1] =
                                                                  identitySelected[
                                                                          indexLevel1] +
                                                                      identitySelected[
                                                                          indexLevel1 +
                                                                              1];
                                                              identitySelected
                                                                  .removeAt(
                                                                      indexLevel1);
                                                            }
                                                            // multiple identities in this priority
                                                            else if (identitySelected[
                                                                        indexLevel1]
                                                                    .length >
                                                                1) {
                                                              final toMove =
                                                                  identitySelected[
                                                                          indexLevel1]
                                                                      .removeAt(
                                                                          indexLevel2);
                                                              identitySelected
                                                                  .insert(
                                                                      indexLevel1 +
                                                                          1,
                                                                      [toMove]);
                                                            }
                                                          });
                                                        },
                                                      ),
                                                      IconButton(
                                                        icon: Icon(Icons.clear),
                                                        iconSize: 14.0,
                                                        color: Colors.grey[600],
                                                        splashColor:
                                                            Colors.transparent,
                                                        highlightColor:
                                                            Colors.transparent,
                                                        tooltip: '移除',
                                                        hoverColor:
                                                            Colors.transparent,
                                                        onPressed: () {
                                                          setState(() {
                                                            if (identitySelected[
                                                                        indexLevel1]
                                                                    .length ==
                                                                1) {
                                                              identitySelected
                                                                  .removeAt(
                                                                      indexLevel1);
                                                            } else {
                                                              identitySelected[
                                                                      indexLevel1]
                                                                  .removeAt(
                                                                      indexLevel2);
                                                            }
                                                          });
                                                        },
                                                      ),
                                                    ],
                                                  ),
                                                ),
                                              );
                                            }),
                                      ),
                                    ],
                                  ),
                                ),
                              );
                            },
                          ),
                        ),
                      ),
                    ],
                  ),
                )),

            // done button
            Expanded(
              flex: 2,
              child: Container(
                padding: EdgeInsets.symmetric(vertical: 15.0),
                child: ButtonTheme(
                  height: 5.0,
                  child: FlatButton(
                    color: isProcessing ? Colors.indigo[900] : Colors.indigo,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(50.0),
                    ),
                    onPressed: () async {
                      setState(() {
                        isProcessing = true;
                      });

                      // get matching result
                      Map result;
                      await getMatchResult(studentData, bedData)
                          .then((response) {
                        if (response.statusCode == 200) {
                          result = jsonDecode(response.body);
                          // result = response.data.cast<String>();
                          for (var k in result.keys) {
                            // print(k);
                            // print(result[k].length);
                          }
                        } else {
                          // TODO: deal with invalid response

                        }
                      });

                      setState(() {
                        isProcessing = false;
                      });

                      // Navigator.pushReplacementNamed(context, '/result');
                      await Navigator.pushNamed(context, '/result',
                          arguments: {'result': result});
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
            ),
          ],
        ),
      ),
    );
  }
}
