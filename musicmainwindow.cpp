#include "musicmainwindow.h"
#include "./ui_musicmainwindow.h"
#include "genericfns.hpp"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    QAction::connect(ui->addsongs, &QAction::triggered, &musicFns->addSongs);
}

MainWindow::~MainWindow()
{
    delete ui;
}

