import 'dart:io';
import 'package:excel/excel.dart';
import '../../conf/dorm_conf.dart';

class FormatData {
  final String dormName;
  List<String> colName = [];
  List<List> _data = [];
  var candidateItem = new Map();

  List<List> data; // filtered Data

  FormatData(this.dormName, dormData) {
    // deal with column
    for (var i = 0; i < dormData[0].length; i++) {
      colName.add(dormData[0][i]);
    }

    // deal with data
    for (var i = 1; i < (dormData.length) - 1; i++) {
      List dataCells = [];
      for (var j = 0; j < (dormData[i].length); j++) {
        dataCells.add(dormData[i][j]);
      }
      _data.add(dataCells);
    }
    // warning: sorting only succeeds when index 0 is "學號"
    _data.sort((a, b) => int.parse(a[0]).compareTo(int.parse(b[0])));
    data = new List<List>.from(_data);

    // deal with candidateItem
    for (var i = 0; i < colName.length; i++) // create new Set for every column
    {
      candidateItem[colName[i]] = new Set();
    }
    for (var i = 1; i < data.length; i++) // update the Set for every column
    {
      for (var j = 0; j < colName.length; j++) {
        candidateItem[colName[j]].add(data[i][j].toString());
      }
    }
    for (var i = 0; i < colName.length; i++) {
      List temp = new List.from(candidateItem[colName[i]].toList());
      candidateItem[colName[i]] = temp;
    }
  }

  int length() {
    return data.length;
  }

  void filterData(Map selectedItem) {
    data = List<List>.from(_data);
    for (var i = _data.length - 1; i >= 0; i--) {
      for (var j = 0; j < colName.length; j++) {
        if (!selectedItem[colName[j]].contains(_data[i][j].toString())) {
          data.removeAt(i);
          break;
        }
      }
    }
  }

  void saveOneData(storePath) {
    var excel = Excel.createExcel();
    Sheet sheet = excel[dorm_eng2chi[dormName]];

    // store columns
    for (var i = 0; i < colName.length; i++) {
      final columnIndex = 'A'.codeUnitAt(0) + i;

      var cell = sheet.cell(
          CellIndex.indexByString(String.fromCharCode(columnIndex) + '1'));
      cell.value = colName[i];
    }

    // store rows
    for (var i = 0; i < data.length; i++) {
      for (var j = 0; j < colName.length; j++) {
        final columnIndex = 'A'.codeUnitAt(0) + j;
        final rowIndex = i + 2;

        final cell_i = String.fromCharCode(columnIndex) + (rowIndex).toString();
        var cell = sheet.cell(CellIndex.indexByString(cell_i));
        cell.value = data[i][j];
      }
    }

    excel.delete("Sheet1");

    excel.encode().then((onValue) {
      File(storePath)
        ..createSync(recursive: true)
        ..writeAsBytesSync(onValue);
    });
  }

  void saveAllHelper(excel) {
    Sheet sheet = excel[dorm_eng2chi[dormName]];
    if (excel.tables.keys.length == 2) {
      excel.setDefaultSheet(dormName).then((isSet) {});
    }

    // store columns
    for (var i = 0; i < colName.length; i++) {
      final columnIndex = 'A'.codeUnitAt(0) + i;

      var cell = sheet.cell(
          CellIndex.indexByString(String.fromCharCode(columnIndex) + '1'));
      cell.value = colName[i];
    }

    // store rows
    for (var i = 0; i < _data.length; i++) {
      for (var j = 0; j < colName.length; j++) {
        final columnIndex = 'A'.codeUnitAt(0) + j;
        final rowIndex = i + 2;

        final cell_i = String.fromCharCode(columnIndex) + (rowIndex).toString();
        var cell = sheet.cell(CellIndex.indexByString(cell_i));
        cell.value = _data[i][j];
      }
    }
  }
}
