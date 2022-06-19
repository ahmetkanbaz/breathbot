import 'package:bubble/bubble.dart';
import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class BreathChat extends StatefulWidget {
  const BreathChat({Key? key}) : super(key: key);

  @override
  _BreathChatState createState() => _BreathChatState();
}

class _BreathChatState extends State<BreathChat> {
  final mesajControl = TextEditingController();
  List<Map> mesajlar = [];

  String chat = "";
  String final_response = "";
  final _formKey = GlobalKey<FormState>();

  Future<void> _savingData() async {
    final validation = _formKey.currentState?.validate();
    if (!validation!) {
      return;
    }
    _formKey.currentState?.save();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.green,
        elevation: 0,
        centerTitle: true,
        title: Text(
          'BreathBot',
          style: TextStyle(fontWeight: FontWeight.bold),
        ),
      ),
      body: Container(
        color: Colors.white,
        child: Column(
          children: <Widget>[
            Center(
              child: Container(
                padding: EdgeInsets.only(top: 20.0, bottom: 15.0),
                child: Text(
                  //Kullanıcının chatbot ile konuşmak için giriş tarihi tutuluyor.
                  'Giriş Saati: ${DateFormat('Hm').format(DateTime.now())}',
                  style: TextStyle(fontSize: 18.0),
                ),
              ),
            ),
            Flexible(
                child: ListView.builder(
              reverse: true,
              itemCount: mesajlar.length,
              itemBuilder: (context, index) => breathChat(
                  mesajlar[index]['mesaj'].toString(),
                  mesajlar[index]['data']),
            )),
            SizedBox(
              height: 20.0,
            ),
            Divider(
              height: 5.0,
              color: Colors.green,
            ),
            Container(
              child: ListTile(
                title: Container(
                  height: 40,
                  decoration: BoxDecoration(
                      borderRadius: BorderRadius.all(Radius.circular(45.0)),
                      color: Colors.grey.shade300,),
                  padding: EdgeInsets.only(left: 15.0),

                  //Kullanıcıdan girdi alınıyor.
                  child: Form(
                    key: _formKey,
                    child: TextFormField(
                      keyboardType: TextInputType.multiline,
                      controller: mesajControl,
                      decoration: InputDecoration(
                        hintText: "Bir Şeyler Yazınız.",
                        hintStyle: TextStyle(
                            color: Colors.black26
                        ),
                        border: InputBorder.none,
                        focusedBorder: InputBorder.none,
                        enabledBorder: InputBorder.none,
                        errorBorder: InputBorder.none,
                        disabledBorder: InputBorder.none,
                      ),
                      onSaved: (value) {
                        chat =
                            value!;
                      },
                      style: TextStyle(fontSize: 16.0, color: Colors.black),
                      onChanged: (value) {},
                    ),
                  ),
                ),
                trailing: IconButton(
                  icon: Icon(
                    Icons.send,
                    size: 30.0,
                    color: Colors.green,
                  ),
                  onPressed: () async {

                    _savingData();

                    //Python ile iletişim kurulabilmesi için url belirleniyor.
                    final url = 'http://10.0.2.2:5000/chat';

                    //Belirlenen url'ye veri göndermek için değişken tanımlıyoruz.
                    final response = await http.post(Uri.parse(url),
                        body: json.encode({'chat': chat}));

                    final responseTemp = await http.get(Uri.parse(url));

                    //Alınan değerin ekranda gösterilmesi için dönüşüm yapılmaktadır.
                    final decoded =
                        json.decode(responseTemp.body) as Map<String, dynamic>;

                    setState(() {
                      //Kullanıcının yazmış olduğu mesaj list'e ekleniyor.
                      mesajlar
                          .insert(0, {"data": 1, "mesaj": mesajControl.text});
                      //Python tarafından alınan cevap değişkene atanıyor.
                      final_response = decoded['chat'];
                      //Python tarafında chatbotun vermiş olduğu cevap mesaj list'e ekleniyor.
                      mesajlar.insert(0, {"data": 0, "mesaj": final_response});
                    });
                    //Kullanıcı chatbota mesaj gönderdikten sonra girdi kısmı temizlenmektedir.
                    mesajControl.clear();
                    FocusScopeNode currentFocus = FocusScope.of(context);
                    if (!currentFocus.hasPrimaryFocus) {
                      currentFocus.unfocus();
                    }
                  },
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }


  //Mesajların kimden geldiğine bağlı olarak tasarımlar gerçekleştirilmektedir.
  //Yani mesajın chatbot veya kullanıcının atıp atmadığına bağlı olarak tasarımlar değişmektedir.
  Widget breathChat(String mesaj, int data) {
    return Container(
      padding: EdgeInsets.only(left: 20.0, right: 20.0),
      child: Row(
        mainAxisAlignment:
            data == 1 ? MainAxisAlignment.end : MainAxisAlignment.start,
        children: <Widget>[
          data == 0
              ? Container(
                  height: 50.0,
                  width: 50.0,
                  child: CircleAvatar(
                    backgroundColor: Colors.transparent,
                    backgroundImage: AssetImage("assets/iconBot.png"), //Chatbottan mesaj geldiyse chatbotun iconu eklenmektedir.
                  ),
                )
              : Container(),
          Padding(
            padding: EdgeInsets.all(10.0),
            child: Bubble(
              radius: Radius.circular(15.0),
              color: data == 0 ? Colors.grey.shade200 : Colors.green.shade400,
              elevation: 0.0,
              child: Padding(
                padding: EdgeInsets.all(2.0),
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: <Widget>[
                    Flexible(
                        child: Container(
                      constraints: BoxConstraints(maxWidth: 200.0),
                      child: Text(
                        mesaj,
                        style: TextStyle(color: Colors.black),
                      ),
                    )),
                  ],
                ),
              ),
            ),
          ),
          data == 1
              ? Container(
                  height: 50.0,
                  width: 50.0,
                  child: CircleAvatar(
                    backgroundColor: Colors.grey.shade300,
                    child: Icon(Icons.person, size: 30.0, color: Colors.black54,), //Mesaj, kullanıcı tarafından geldiyse 'person' ikonu eklenmektedir.
                  ),
                )
              : Container(),
        ],
      ),
    );
  }
}
