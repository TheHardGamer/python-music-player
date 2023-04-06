#ifndef MUSICMAINWINDOW_H
#define MUSICMAINWINDOW_H

#include <QMainWindow>

QT_BEGIN_NAMESPACE
namespace Ui { class MusicMainWindow; }
QT_END_NAMESPACE

class MusicMainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MusicMainWindow(QWidget *parent = nullptr);
    ~MusicMainWindow();

private:
    Ui::MusicMainWindow *ui;
};
#endif // MUSICMAINWINDOW_H
