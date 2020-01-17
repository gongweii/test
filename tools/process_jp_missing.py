import pdb
missing_file = "/home/wgong/tt/earlier_res/jp_result/missing"

missing_list = []
with open(missing_file,"r",encoding="utf-8") as inf:
  for line in inf:
    if line.find("平成") != -1:
      continue
    if line.find("取締役に対するストックオプション") != -1:
      continue
    if line.find("主要株主の異動(予定)に関") != -1:
      continue
    if line.find("第三者割当による自己株式処分の") != -1:
      continue
    if line.find("ストック・オプション(新株予約権)") != -1:
      continue
    if line.find("特別損失") != -1:
      continue
    if line.find("人事異動に関") != -1:
      continue
    if line.find("公益財団法人 財務会計基準機構へ") != -1:
      continue
    if line.find("支配株主等に関する事項") != -1:
      continue
    if line.find("人事に関するお知") != -1:
      continue
    if line.find("回無担保社債発行") != -1:
      continue
    if line.find("資金の借入および返済に関") != -1:
      continue
    if line.find("第三者割当による新株式発行の払込完了に関") != -1:
      continue
    if line.find("組織の改編および人事異動") != -1:
      continue
    if line.find("大阪証券取引所") != -1:
      continue
    if line.find("決算期変更及び定款一部変更に関") != -1:
      continue
    if line.find("G7 Political") != -1:
      continue
    if line.find("本日の一部報道について") != -1:
      continue
    if line.find("自己株式の取得状況および取得終了に関") != -1:
      continue
    if line.find("当社株式の貸借銘柄選定に関") != -1:
      continue
    if line.find("自己株式立会外買付取引(ToSTNeT-3)による自己株式") != -1:
      continue
    if line.find("当社株式の大規模買付行為への対応策(買収防衛策)") != -1:
      continue
    if line.find("資金の借入に関") != -1:
      continue
    if line.find("当社第一回優先株式の転換価額の") != -1:
      continue
    if line.find("剰余金の配当に関") != -1:
      continue
    if line.find("訂正・数値データ訂正あり") != -1:
      continue
    if line.find("上場申請会社概要") != -1:
      continue
    if line.find("役員の変更について") != -1:
      continue
    if line.find("自己株式立会外買付取引(ToSTNeT-3)による自己株式の買付けに関") != -1:
      continue
    if line.find("取締役候補者の変更及び役員の異動に関するお知") != -1:
      continue
    if line.find("代表取締役及び役職の異動に関") != -1:
      continue
    if line.find("株主優待制度の変更に関") != -1:
      continue
    if line.find("定款一部変更に関するお知ら") != -1:
      continue
    if line.find("第三社割当による新株予約権の行使期間満")!=-1:
      continue
    if line.find("執行役に関するお知らせ") != -1:
      continue
    if line.find("合弁会社設立に関するお知らせ") != -1:
      continue
    if line.find("監査役の異動に関するお知らせ")  != -1:
      continue
    if line.find("人事の異動に関するお知らせ") != -1:
      continue
    if line.find("連結子会社の合併および商号変更に関するお知") != -1:
      continue
    if line.find("執行役の異動について") != -1:
      continue
    if line.find("公認会計士等の異動に関するお知ら")!=-1:
      continue
    if line.find("自己株式の取得結果に関するお知") != -1:
      continue
    if line.find("組織変更及び役員の異動に関するお")!=-1:
      continue
    if line.find("連結子会社の株式の譲渡に関するお") != -1:
      continue
    if line.find("役員の異動に関するお知らせ") != -1:
      continue
    if line.find("定款一部変更のお知らせ") != -1:
      continue
    if line.find("業務組織改定などに関するお知ら") != -1:
      continue
    if line.find("公募による新株式発行の中止に") != -1:
      continue
    if line.find("取締役及び監査役の辞任に関") != -1:
      continue
    if line.find("資本準備金の額の減少に関す") != -1:
      continue
    if line.find("売出価格等の決定に関するお") != -1:
      continue
    if line.find("代表執行役の異動について") != -1:
      continue
    if line.find("第7期決算説明会資料") != -1:
      continue
    if line.find("主要株主である筆頭株主の異動に関するお知") != -1:
      continue
    if line.find("役員報酬等の減額に関するお知") != -1:
      continue
    if line.find("特別利益の金額の変更") != -1:
      continue
    if line.find("主要株主の異動に関するお知") != -1:
      continue
    if line.find("第三者割当により発行される株式の払込完了に関す") != -1:
      continue
    if line.find("役員の異動について") != -1:
      continue
    if line.find("臨時株主総会") != -1:
      continue
    if line.find("訴訟の提起に関するお知") != -1:
      continue
    if line.find("本日の一部報道について")!=-1:
      continue
    if line.find("株式報酬型ストックオプション(新株予約権)")!=-1:
      continue
    if line.find("決算概要")!=-1:
      continue
    if line.find("決算説明会")!=-1:
      continue
    if line.find("剰余金の配当に関する") != -1:
      continue
    if line.find("業務改善計画の提出に")!=-1:
      continue
    if line.find("剰余金の配当に関するお知らせ")!=-1:
      continue
    if line.find("新株予約権(株式報酬型ストックオプション)の発行")!=-1:
      continue
    if line.find("特別利益の計上に関")!=-1:
      continue
    if line.find("記念配当の実施に関") != -1:
      continue
    if line.find("無担保社債の発行に") != -1:
      continue
    if line.find("第三者割当による自己株式の処分に関する") != -1:
      continue
    if line.find("株式売出しに関するお知らせ")!= -1:
      continue
    if line.find("新規店舗のお知らせ") != -1:
      continue
    if line.find("本日の一部報道について")!=-1:
      continue
    if line.find("ストックオプション(新株予約権)")!=-1:
      continue
    if line.find("本店移転に関するお知らせ")!=-1:
      continue
    if line.find("役員人事内定のお知らせ") != -1:
      continue
    if line.find("自己株式の取得状況に関")!=-1:
      continue
    if line.find("自己株式の取得に関するお知")!=-1:
      continue
    if line.find("自己株式の市場買付けに関する") != -1:
      continue
    if line.find("日々の一口あたりの参考価額") != -1:
      continue
    if line.find("公益財団法人財務会計基準機構へ")!=-1:
      continue
    if line.find("月次販売実績のお知らせ")!=-1:
      continue
    if line.find("定款の一部変更に関するお知らせ") != -1:
      continue
    if line.find("当社社長人事に関する一部報道に")!=-1:
      continue
    if line.find("資金の借入(金利決定)に関す")!=-1:
      continue
    if line.find("代表取締役の異動に関するお知")!=-1:
      continue
    if line.find("株主優待制度の一部変更に関するお知")!=-1:
      continue
    if line.find("取締役辞任に関するお知ら")!=-1:
      continue
    if line.find("役員の異動及び機構改革に関するお知")!=-1:
      continue
    if line.find("短期借入金の金利決定に関するお知")!=-1:
      continue
    if line.find("定款の一部変更(取締役の任期変更)に関する")!=-1:
      continue
    if line.find("代表取締役の異動および取締役候補の選任に関するお")!=-1:
      continue
    if line.find("転換社債型新株予約権付社債の発行条件等の決定")!=-1:
      continue
    if line.find("資本金の額の減少に関するお知ら")!=-1:
      continue
    if line.find("月次売上高前年比情報に関するお知")!=-1:
      continue
    if line.find("機構改革に関するお知ら")!=-1:
      continue
    if line.find("代表取締役の異動および取締役の異動につ")!=-1:
      continue
    if line.find("担保設定に係る契約締結に関するお")!=-1:
      continue
    if line.find("固定資産の取得に関するお知らせ")!=-1:
      continue
    if line.find("機構改革および人事異動につ")!=-1:
      continue
    if line.find("第三者割当による自己株式処分に関するお知")!=-1:
      continue
    if line.find("役員の管掌変更に関するお知らせ")!=-1:
      continue
    if line.find("監査役選任に関するお知らせ")!=-1:
      continue
    if line.find("人事異動のお知らせ")!=-1:
      continue
    if line.find("役員の異動ならびに組織変更に関するお知らせ")!=-1:
      continue
    if line.find("自己株式の消却に関するお知らせ")!=-1:
      continue
    if line.find("自己株式取得に係る事項の決定に関するお知")!=-1:
      continue
    if line.find("決算発表資料の追加(役員の異動)に関するお知")!=-1:
      continue
    if line.find("子会社の減損損失に関するお知らせ")!=-1:
      continue
    if line.find("連結子会社間の合併に関するお知らせ")!=-1:
      continue
    if line.find("子会社間の合併のお知らせ")!=-1:
      continue
    if line.find("人事異動及び組織変更に関するお知らせ")!=-1:
      continue
    if line.find("代表取締役又は代表執行役の異動等について")!=-1:
      continue
    if line.find("執行役の異動に関するお知らせ")!=-1:
      continue
    if line.find("電子公告のアドレス変更に関するお知らせ")!=-1:
      continue
    if line.find("執行役の異動に関するお知らせ")!=-1:
      continue
    if line.find("業績予想との差異に関するお知らせ")!=-1:
      continue
    if line.find("親会社等の決算に関するお知らせ")!=-1:
      continue
    if line.find("組織変更および人事異動について")!=-1:
      continue
    if line.find("一部報道について(英語)")!=-1:
      continue
    if line.find("役員の異動に関する件お知らせ")!=-1:
      continue
    if line.find("コーポレート・ガバナンスに関")!=-1:
      continue
    if line.find("TDnet開示情報の修正について")!=-1:
      continue
    if line.find("TDnet開示情報の削除、再登録について")!=-1:
      continue
    if line.find("TDnetシステム稼動確認データ")!=-1:
      continue

    missing_list.append(line.strip())

missing_file = "missing"
with open(missing_file,"a",encoding="utf-8") as outf:
  for line in missing_list:
    print(line.strip(),file = outf)
    
