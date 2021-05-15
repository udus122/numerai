# numerai

## Directory Sturcture

```plaintext
.
├── data               #  データ格納するdirectory(共有しない)
│   ├── raw           #  生データを格納するdirectory
│   ├── features      #  特徴量を格納するdirectory
│   ├── output        #  出力データ(Submissionファイルなど)を格納するdirectory
│   ├── archive       #  不要になったデータを格納するdirectory
├── notebooks          #  作業中のipynbをこのディレクトリに入れておくINBOX的なディレクトリ
│   ├── archive       #  もう使わないipynbを置くdirectory
│   └── eda           #  後で見返したいEDAのipynbを置くdirectory
└── src                #  コード(.py)を置くdirectory
│   ├── libs          #  使いまわしたいモジュールを置くdirectory
│   │   ├── features #  特徴量作成用のモジュールを置くdirectory
│   │   ├── models   #  モデル作成のモジュールを置くdirectory
│   │   └── utils    #  汎用的に使えるモジュールを置くdirectory
│   ├── config        #  プロジェクト全体で使い回す設定
└── logs               #  log全般
└── models             #  modelを保存するdirectory
```
