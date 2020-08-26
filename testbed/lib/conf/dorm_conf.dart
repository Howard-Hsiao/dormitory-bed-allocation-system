// Specify the name of every dormitory
const String boyDorm = 'men_campus_dorm';
const String girlDorm = 'women_campus_dorm';
const String bot_boy = 'men_BOT'; // 長興
const String bot_girl = 'women_BOT'; // 水源

const List<String> dataName = [boyDorm, girlDorm, bot_boy, bot_girl];

// chinese name
const String chi_boyDorm = '男生宿舍';
const String chi_girlDorm = '女生宿舍';
const String chi_bot_boy = 'BOT男生宿舍'; // 長興
const String chi_bot_girl = 'BOT女生宿舍'; // 水源

const List<String> chi_dataName = [
  chi_boyDorm,
  chi_girlDorm,
  chi_bot_boy,
  chi_bot_girl
];

const Map dorm_eng2chi = {
  boyDorm: chi_boyDorm,
  girlDorm: chi_girlDorm,
  bot_boy: chi_bot_boy,
  bot_girl: chi_bot_girl
};

const Map dorm_chi2eng = {
  chi_boyDorm: boyDorm,
  chi_girlDorm: girlDorm,
  chi_bot_boy: bot_boy,
  chi_bot_girl: bot_girl
};
