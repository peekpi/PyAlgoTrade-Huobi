#ifndef QUSERASSET_H
#define QUSERASSET_H

#include <QObject>
#ifdef Q_OS_WIN
#include <QtNetwork/QNetworkAccessManager>
#include <QtNetwork/QNetworkReply>
#else
#include <QNetworkAccessManager>
#include <QNetworkReply>
#endif
#include <QJsonObject>
#include <QJsonDocument>
#include "defines.h"

class QUserAsset : public QObject
{
    Q_OBJECT
public:
    explicit QUserAsset(QObject *parent = 0);
    ~QUserAsset();

    void get();

    QJsonObject userAssetInfo;
private:
    QNetworkAccessManager * _manager;
signals:
    //data update
    void updated(QJsonObject &userAssetInfo);
public slots:
private slots:
    void onFinished(QNetworkReply * reply);
};

#endif // QUSERASSET_H
