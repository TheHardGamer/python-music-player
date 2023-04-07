#ifndef MUSICMAINWINDOW_H
#define MUSICMAINWINDOW_H

#include "genericfns.hpp"
QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private:
    Ui::MainWindow *ui;
    genericFns *musicFns = genericFns::getInstance();
};
#endif // MUSICMAINWINDOW_H
