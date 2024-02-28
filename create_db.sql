CREATE TABLE "staff" (
	"id"	INTEGER NOT NULL UNIQUE,
	"first_name"	TEXT NOT NULL,
	"last_name"	TEXT NOT NULL,
	"patronymic"	TEXT,
	"job"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
)