#include "musicmainwindow.h"
#include "./ui_musicmainwindow.h"

MusicMainWindow::MusicMainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MusicMainWindow)
{
    ui->setupUi(this);
}

MusicMainWindow::~MusicMainWindow()
{
    delete ui;
}

