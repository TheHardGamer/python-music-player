#include "musicmainwindow.h"

#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MusicMainWindow w;
    w.show();
    return a.exec();
}
