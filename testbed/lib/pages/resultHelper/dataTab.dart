import 'package:flutter/material.dart';
import 'package:flutter_material_pickers/flutter_material_pickers.dart';
import 'package:sprintf/sprintf.dart';
import 'package:file_chooser/file_chooser.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';

import '../../conf/dorm_conf.dart';
import '../../conf/UI_conf.dart';
import './formatData.dart';

class DataTab extends StatefulWidget {
  FormatData dormData;

  DataTab(dormName, data) {
    // deal with column
    dormData = new FormatData(dormName, data);
  }

  @override
  _DataTabState createState() => _DataTabState();
}

class _DataTabState extends State<DataTab> {
  int dataSizePerPage = 15;
  List<String> pageList;
  String curr_page_str = '1';
  Map selectedItem = new Map();
  List<DataColumn> colName = [];
  List<DataRow> displayRows = [];

  TextEditingController _pageSizeController;

  void initState() {
    super.initState();
    _pageSizeController = TextEditingController();
  }

  void dispose() {
    _pageSizeController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    /*page num*/
    final curr_page = int.parse(curr_page_str);
    final start = dataSizePerPage * (curr_page - 1) + 1;
    var end = dataSizePerPage * curr_page;
    if (end > widget.dormData.length()) {
      end = widget.dormData.length();
    }

    /*page list*/
    var pageNum = widget.dormData.length() ~/ dataSizePerPage;
    if (widget.dormData.length() % dataSizePerPage != 0) {
      pageNum++;
    }
    pageList = new List<String>.generate(pageNum, (i) => (i + 1).toString());

    /* deal with displaying data*/
    // initialized selectedItem
    if (selectedItem.length == 0) {
      for (var i = 0; i < widget.dormData.colName.length; i++) {
        selectedItem[widget.dormData.colName[i]] = List<String>();
        final colName_i = widget.dormData.colName[i];
        for (var j = 0;
            j < widget.dormData.candidateItem[colName_i].length;
            j++) {
          selectedItem[colName_i]
              .add(widget.dormData.candidateItem[colName_i][j].toString());
        }
      }
    }

    // initialize column
    colName.clear();
    for (var i = 0; i < widget.dormData.colName.length; i++) {
      colName.add(
        DataColumn(
            label: Row(
              children: <Widget>[
                GestureDetector(
                  child: Row(children: [
                    Text(
                      widget.dormData.colName[i] + "  ",
                      style: ui_text.general_b,
                    ),
                    FaIcon(FontAwesomeIcons.filter,
                        color: Colors.blue, size: 10)
                  ]),
                  onTap: () {
                    showMaterialCheckboxPicker(
                      context: context,
                      title: widget.dormData.colName[i],
                      items: new List<String>.from(widget
                          .dormData.candidateItem[widget.dormData.colName[i]]),
                      selectedItems: selectedItem[widget.dormData.colName[i]],
                      onChanged: (value) => setState(() {
                        selectedItem[widget.dormData.colName[i]] =
                            new List<String>.from(value);
                        widget.dormData.filterData(selectedItem);
                        resetData();
                      }),
                    );
                  },
                )
              ],
            ),
            numeric: false),
      );
    }
    updateData();

    return SingleChildScrollView(
        scrollDirection: Axis.vertical,
        child: Column(
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Container(
                    padding: EdgeInsets.symmetric(horizontal: 13.0),
                    child: Row(children: [
                      Text("每頁顯示 "),
                      Container(
                          width: 35,
                          child: TextField(
                              textInputAction: TextInputAction.next,
                              onSubmitted: (String value) => setState(() {
                                    final newSize = int.parse(value);
                                    if (newSize <= widget.dormData.length()) {
                                      dataSizePerPage = int.parse(value);
                                      resetData();
                                    }
                                  }),
                              controller: _pageSizeController,
                              decoration: InputDecoration.collapsed(
                                  hintText: dataSizePerPage.toString()))),
                      Text(sprintf('筆，目前顯示第%d至第%d筆。共%d頁，%d筆',
                          [start, end, pageNum, widget.dormData.length()])),
                    ])),
                Container(
                    padding: EdgeInsets.only(right: 10.0),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                      children: [
                        RaisedButton(
                          child: Row(children: [
                            Text(
                              '選擇頁數',
                              style: ui_text.general_b,
                            ),
                            Icon(
                              Icons.arrow_drop_down,
                              color: Colors.blue,
                            )
                          ]),
                          onPressed: () => showMaterialScrollPicker(
                            context: context,
                            title: '選擇頁數',
                            items: pageList,
                            selectedItem: curr_page_str,
                            onChanged: (value) => setState(() {
                              curr_page_str = value;
                              updateData();
                            }),
                          ),
                        ),
                        RaisedButton(
                            onPressed: () {
                              showSavePanel(
                                      suggestedFileName: dorm_eng2chi[
                                              widget.dormData.dormName] +
                                          '.xlsx')
                                  .then((result) {
                                widget.dormData.saveOneData(result.paths[0]);
                              });
                            },
                            child: Padding(
                              padding: EdgeInsets.all(5.0),
                              child: Text(
                                '匯出此表',
                                style: ui_text.general_b,
                              ),
                            ))
                      ],
                    ))
              ],
            ),
            SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: DataTable(
                    onSelectAll: (b) {}, //!!!!!!!!!???
                    sortColumnIndex: 1,
                    sortAscending: true,
                    columns: colName,
                    rows: displayRows))
          ],
        ));
  }

  void updateData() {
    displayRows.clear();

    final currPage = int.parse(curr_page_str);
    final start = (currPage - 1) * dataSizePerPage;
    final end = (start + dataSizePerPage < widget.dormData.length())
        ? (start + dataSizePerPage)
        : widget.dormData.length();

    for (var i = start; i < end; i++) {
      List<DataCell> dataCells = [];
      for (var j = 0; j < (widget.dormData.data[i].length); j++) {
        dataCells.add(DataCell(
            Text(
              widget.dormData.data[i][j].toString(),
              style: ui_text.general_b,
            ),
            showEditIcon: false,
            placeholder: false));
      }
      displayRows.add(DataRow(cells: dataCells));
    }
  }

  void resetData() {
    var pageNum = widget.dormData.length() ~/ dataSizePerPage;
    if (widget.dormData.length() % dataSizePerPage != 0) {
      pageNum++;
    }
    pageList = new List<String>.generate(pageNum, (i) => (i + 1).toString());
    curr_page_str = '1';

    updateData();
  }

  void saveThisData() {}
}
