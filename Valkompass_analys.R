library(stringr)
library(odbc)
library(DBI)
library(ggplot2)
library(tidyverse)
library(lapply)
library(ggplot2)

#KEEP IN MIND THAT IM USED TO CODING IN PYTHON AND R SUCKS AT FOR LOOPS. THIS CODE DID THE WORK BUT IS REALLY UGLY. GO TO MY PYTHON SCRIPT FOR HOT STUFF. 

#setting up connection

con <- dbConnect(odbc::odbc(), .connection_string = "Driver={MySQL ODBC 8.0 Unicode Driver};",
                 Server = 'localhost', Database='valkompasser',UID='root', PWD='Ask me at malte.meuller@gmail.com', Port=3306)


#laddar ner datafilerna
aftonbladet <- dbReadTable(con, 'aftonbladet')
arbetet <- dbReadTable(con, 'arbetet')
di <- dbReadTable(con, 'di')
dn<- dbReadTable(con, 'dn')
foretagarna <- dbReadTable(con, 'foretagarna')
svt<- dbReadTable(con, 'svt')
valkompassen <- dbReadTable(con, 'valkompassen')

#only use 500 observations to be able to compare. 
aftonbladet <- aftonbladet %>%slice(1:500)
arbetet <- arbetet %>%slice(1:500)
di <- di %>%slice(1:500)
dn <- dn %>%slice(1:500)
foretagarna <- foretagarna %>%slice(1:500)
svt <- svt %>%slice(1:500)
valkompassen <- valkompassen %>%slice(1:500)


#rescale so mean =100, use same multiplier for all. 
mean_aftonbladet <-colMeans(aftonbladet)
aftonbladet$V <- aftonbladet$V *(100/mean(mean_aftonbladet))
aftonbladet$S <- aftonbladet$S *(100/mean(mean_aftonbladet))
aftonbladet$MP <- aftonbladet$MP *(100/mean(mean_aftonbladet))
aftonbladet$C <- aftonbladet$C *(100/mean(mean_aftonbladet))
aftonbladet$L <- aftonbladet$L *(100/mean(mean_aftonbladet))
aftonbladet$M <- aftonbladet$M *(100/mean(mean_aftonbladet))
aftonbladet$KD <- aftonbladet$KD *(100/mean(mean_aftonbladet))
aftonbladet$SD <- aftonbladet$SD *(100/mean(mean_aftonbladet))

mean_arbetet <-colMeans(arbetet)
arbetet$V <- arbetet$V *(100/mean(mean_arbetet))
arbetet$S <- arbetet$S *(100/mean(mean_arbetet))
arbetet$MP <- arbetet$MP *(100/mean(mean_arbetet))
arbetet$C <- arbetet$C *(100/mean(mean_arbetet))
arbetet$L <- arbetet$L *(100/mean(mean_arbetet))
arbetet$M <- arbetet$M *(100/mean(mean_arbetet))
arbetet$KD <- arbetet$KD *(100/mean(mean_arbetet))
arbetet$SD <- arbetet$SD *(100/mean(mean_arbetet))

mean_di <-colMeans(di)
di$V <- di$V *(100/mean(mean_di))
di$S <- di$S *(100/mean(mean_di))
di$MP <- di$MP *(100/mean(mean_di))
di$C <- di$C *(100/mean(mean_di))
di$L <- di$L *(100/mean(mean_di))
di$M <- di$M *(100/mean(mean_di))
di$KD <- di$KD *(100/mean(mean_di))
di$SD <- di$SD *(100/mean(mean_di))

mean_dn <-colMeans(dn)
dn$V <- dn$V *(100/mean(mean_dn))
dn$S <- dn$S *(100/mean(mean_dn))
dn$MP <- dn$MP *(100/mean(mean_dn))
dn$C <- dn$C *(100/mean(mean_dn))
dn$L <- dn$L *(100/mean(mean_dn))
dn$M <- dn$M *(100/mean(mean_dn))
dn$KD <- dn$KD *(100/mean(mean_dn))
dn$SD <- dn$SD *(100/mean(mean_dn))

mean_foretagarna <-colMeans(foretagarna)
foretagarna$V <- foretagarna$V *(100/mean(mean_foretagarna))
foretagarna$S <- foretagarna$S *(100/mean(mean_foretagarna))
foretagarna$MP <- foretagarna$MP *(100/mean(mean_foretagarna))
foretagarna$C <- foretagarna$C *(100/mean(mean_foretagarna))
foretagarna$L <- foretagarna$L *(100/mean(mean_foretagarna))
foretagarna$M <- foretagarna$M *(100/mean(mean_foretagarna))
foretagarna$KD <- foretagarna$KD *(100/mean(mean_foretagarna))
foretagarna$SD <- foretagarna$SD *(100/mean(mean_foretagarna))

mean_svt <-colMeans(svt)
svt$V <- svt$V *(100/mean(mean_svt))
svt$S <- svt$S *(100/mean(mean_svt))
svt$MP <- svt$MP *(100/mean(mean_svt))
svt$C <- svt$C *(100/mean(mean_svt))
svt$L <- svt$L *(100/mean(mean_svt))
svt$M <- svt$M *(100/mean(mean_svt))
svt$KD <- svt$KD *(100/mean(mean_svt))
svt$SD <- svt$SD *(100/mean(mean_svt))

mean_valkompassen <-colMeans(valkompassen)
valkompassen$V <- valkompassen$V *(100/mean(mean_valkompassen))
valkompassen$S <- valkompassen$S *(100/mean(mean_valkompassen))
valkompassen$MP <- valkompassen$MP *(100/mean(mean_valkompassen))
valkompassen$C <- valkompassen$C *(100/mean(mean_valkompassen))
valkompassen$L <- valkompassen$L *(100/mean(mean_valkompassen))
valkompassen$M <- valkompassen$M *(100/mean(mean_valkompassen))
valkompassen$KD <- valkompassen$KD *(100/mean(mean_valkompassen))
valkompassen$SD <- valkompassen$SD *(100/mean(mean_valkompassen))



#lägg till namn på de olika kompasserna
aftonbladet$valkompass <- 'aftonbladet'
arbetet$valkompass <- 'arbetet'
aftonbladet$valkompass <- 'aftonbladet'
di$valkompass <- 'di'
foretagarna$valkompass <- 'foretagarna'
svt$valkompass <- 'svt'
valkompassen$valkompass <- 'valkompassen'



#skapar nya datatable där den som har högst får 1 osv. 
df_aftonbladet = data.frame()
for (i in 1:nrow(aftonbladet)) {
  output = sort(aftonbladet[i,1:8], decreasing = TRUE)
  output2 = colnames(output)
  df_aftonbladet = rbind(df_aftonbladet, output2)}
colnames(df_aftonbladet)<-c('first', 'second', 'third', 'fourth', 'fifth', 'sixt', 'seventh', 'eight')
p_aftonbladet <- df_aftonbladet

df_arbetet = data.frame()
for (i in 1:nrow(arbetet)) {
  output = sort(arbetet[i,1:8], decreasing = TRUE)
  output2 = colnames(output)
  df_arbetet = rbind(df_arbetet, output2)}
colnames(df_arbetet)<-c('first', 'second', 'third', 'fourth', 'fifth', 'sixt', 'seventh', 'eight')
p_arbetet <- df_arbetet

df_di = data.frame()
for (i in 1:nrow(di)) {
  output = sort(di[i,1:8], decreasing = TRUE)
  output2 = colnames(output)
  df_di = rbind(df_di, output2)}
colnames(df_di)<-c('first', 'second', 'third', 'fourth', 'fifth', 'sixt', 'seventh', 'eight')
p_di <- df_di

df_dn = data.frame()
for (i in 1:nrow(dn)) {
  output = sort(dn[i,1:8], decreasing = TRUE)
  output2 = colnames(output)
  df_dn = rbind(df_dn, output2)}
colnames(df_dn)<-c('first', 'second', 'third', 'fourth', 'fifth', 'sixt', 'seventh', 'eight')
p_dn <- df_dn

df_foretagarna = data.frame()
for (i in 1:nrow(foretagarna)) {
  output = sort(foretagarna[i,1:8], decreasing = TRUE)
  output2 = colnames(output)
  df_foretagarna = rbind(df_foretagarna, output2)}
colnames(df_foretagarna)<-c('first', 'second', 'third', 'fourth', 'fifth', 'sixt', 'seventh', 'eight')
p_foretagarna <- df_foretagarna

df_svt = data.frame()
for (i in 1:nrow(svt)) {
  output = sort(svt[i,1:8], decreasing = TRUE)
  output2 = colnames(output)
  df_svt = rbind(df_svt, output2)}
colnames(df_svt)<-c('first', 'second', 'third', 'fourth', 'fifth', 'sixt', 'seventh', 'eight')
p_svt <- df_svt

df_valkompassen = data.frame()
for (i in 1:nrow(valkompassen)) {
  output = sort(valkompassen[i,1:8], decreasing = TRUE)
  output2 = colnames(output)
  df_valkompassen = rbind(df_valkompassen, output2)}
colnames(df_valkompassen)<-c('first', 'second', 'third', 'fourth', 'fifth', 'sixt', 'seventh', 'eight')
p_valkompassen <- df_valkompassen


#pivot till längre format för x (de vanliga)
aftonbladet <- aftonbladet %>% pivot_longer(cols = c(1:8), values_to="Poang", names_to='Partier')
arbetet <- arbetet %>% pivot_longer(cols = c(1:8), values_to="Poang", names_to='Partier')
di <- di %>% pivot_longer(cols = c(1:8), values_to="Poang", names_to='Partier')
dn <- dn %>% pivot_longer(cols = c(1:8), values_to="Poang", names_to='Partier')
svt <- svt %>% pivot_longer(cols = c(1:8), values_to="Poang", names_to='Partier')
valkompassen <- valkompassen %>% pivot_longer(cols = c(1:8), values_to="Poang", names_to='Partier')
foretagarna <- foretagarna %>% pivot_longer(cols = c(1:8), values_to="Poang", names_to='Partier')

#pivot till längre format för p_x (positionen)
p_aftonbladet <- p_aftonbladet %>% pivot_longer(cols = c(1:8), values_to = 'party', names_to = 'place')
p_arbetet <- p_arbetet %>% pivot_longer(cols = c(1:8), values_to = 'party', names_to = 'place')
p_di <- p_di %>% pivot_longer(cols = c(1:8), values_to = 'party', names_to = 'place')
p_dn <- p_dn %>% pivot_longer(cols = c(1:8), values_to = 'party', names_to = 'place')
p_svt <- p_svt %>% pivot_longer(cols = c(1:8), values_to = 'party', names_to = 'place')
p_valkompassen <- p_valkompassen %>% pivot_longer(cols = c(1:8), values_to = 'party', names_to = 'place')
p_foretagarna <- p_foretagarna %>% pivot_longer(cols = c(1:8), values_to = 'party', names_to = 'place')

#boxplot med scalade värden
aftonbladet%>% ggplot(aes(x=Partier, y=Poang))+
  geom_boxplot()+
  stat_summary(fun = median, geom = "point", col = "red") +  # Add points to plot
  stat_summary(fun = median, geom = "text", col = "red",     # Add text to plot
               vjust = 1.5, aes(label = paste( round(..y.., digits = 1))))+
  ggtitle("Aftonbladet") +
  ylab("Poäng")
  

arbetet%>%  ggplot(aes(x=Partier, y=Poang))+
  geom_boxplot()+
  stat_summary(fun = median, geom = "point", col = "red") +  # Add points to plot
  stat_summary(fun = median, geom = "text", col = "red",     # Add text to plot
               vjust = 1.5, aes(label = paste( round(..y.., digits = 1))))+
ggtitle("Arbetet") +
  ylab("Poäng")

di%>%  ggplot(aes(x=Partier, y=Poang))+
  geom_boxplot()+
  stat_summary(fun = median, geom = "point", col = "red") +  # Add points to plot
  stat_summary(fun = median, geom = "text", col = "red",     # Add text to plot
               vjust = 1.5, aes(label = paste( round(..y.., digits = 1))))+
  ggtitle("Dagens Industri")+
  ylab("Poäng")

dn%>%  ggplot(aes(x=Partier, y=Poang))+
  geom_boxplot()+
  stat_summary(fun = median, geom = "point", col = "red") +  # Add points to plot
  stat_summary(fun = median, geom = "text", col = "red",     # Add text to plot
               vjust = 1.5, aes(label = paste( round(..y.., digits = 1))))+
  ggtitle("Dagens Nyheter")+
  ylab("Poäng")

foretagarna%>% ggplot(aes(x=Partier, y=Poang))+
  geom_boxplot()+
  stat_summary(fun = median, geom = "point", col = "red") +  # Add points to plot
  stat_summary(fun = median, geom = "text", col = "red",     # Add text to plot
               vjust = 1.5, aes(label = paste( round(..y.., digits = 1))))+
  ggtitle("Företagarna")+
  ylab("Poäng")

svt%>%  ggplot(aes(x=Partier, y=Poang))+
  geom_boxplot()+
  stat_summary(fun = median, geom = "point", col = "red") +  # Add points to plot
  stat_summary(fun = median, geom = "text", col = "red",     # Add text to plot
               vjust = 1.5, aes(label = paste( round(..y.., digits = 1))))+
  ggtitle("SVT")+
  ylab("Poäng")

valkompassen%>%  ggplot(aes(x=Partier, y=Poang))+
  geom_boxplot()+
  stat_summary(fun = median, geom = "point", col = "red") +  # Add points to plot
  stat_summary(fun = median, geom = "text", col = "red",     # Add text to plot
               vjust = 1.5, aes(label = paste( round(..y.., digits = 1))))+
  ggtitle("Valkompassen")+
  ylab("Poäng")

#barchart med placeringarna
p_aftonbladet %>% filter(place=='first') %>% count(party)%>% mutate(percent = 100*n/sum(n))%>%
  ggplot(aes(x=party, y=percent))+
  geom_bar(stat = "identity")+ 
  ggtitle("Aftonbladet")+
  ylim(0, 25)+
  ylab("Procent")+
  geom_text(aes(label=percent), vjust=-1)+
  geom_hline(yintercept =12.5)


p_arbetet %>% filter(place=='first') %>% count(party)%>% mutate(percent = 100*n/sum(n))%>%
  ggplot(aes(x=party, y=percent))+
  geom_bar(stat = "identity")+ 
  ggtitle("Arbetet")+
  ylim(0, 25)+
  ylab("Procent")+
  geom_text(aes(label=percent), vjust=-1)+
  geom_hline(yintercept =12.5)

p_di %>% filter(place=='first') %>% count(party)%>% mutate(percent = 100*n/sum(n))%>%
  ggplot(aes(x=party, y=percent))+
  geom_bar(stat = "identity")+ 
  ggtitle("Dagens Industri")+
  ylim(0, 25)+
  ylab("Procent")+
  geom_text(aes(label=percent), vjust=-1)+
  geom_hline(yintercept =12.5)

p_dn %>% filter(place=='first') %>% count(party)%>% mutate(percent = 100*n/sum(n))%>%
  ggplot(aes(x=party, y=percent))+
  geom_bar(stat = "identity")+ 
  ggtitle("Dagens Nyheter")+
  ylim(0, 25)+
  ylab("Procent")+
  geom_text(aes(label=percent), vjust=-1)+
  geom_hline(yintercept =12.5)

p_foretagarna %>% filter(place=='first') %>% count(party)%>% mutate(percent = 100*n/sum(n))%>%
  ggplot(aes(x=party, y=percent))+
  geom_bar(stat = "identity")+ 
  ggtitle("Foretagarna")+
  ylim(0, 25)+
  ylab("Procent")+
  geom_text(aes(label=percent), vjust=-1)+
  geom_hline(yintercept =12.5)

p_svt %>% filter(place=='first') %>% count(party)%>% mutate(percent = 100*n/sum(n))%>%
  ggplot(aes(x=party, y=percent))+
  geom_bar(stat = "identity")+ 
  ggtitle("SVT")+
  ylim(0, 25)+
  ylab("Procent")+
  geom_text(aes(label=percent), vjust=-1)+
  geom_hline(yintercept =12.5)

p_valkompassen %>% filter(place=='first') %>% count(party)%>% mutate(percent = 100*n/sum(n))%>%
  ggplot(aes(x=party, y=percent))+
  geom_bar(stat = "identity")+ 
  ggtitle("Valkompassen")+
  ylim(0, 25)+
  ylab("Procent")+
  geom_text(aes(label=percent), vjust=-1)+
  geom_hline(yintercept =12.5)


#table 1 and 2
Valkompasser <- c("Aftonbladet", "Arbetet",
                  "Dagens Industri", "Dagens Nyheter","Foretagarna", "SVT", "Valkompassen", "Skillnad")

C <- c("13.2","12","10.6","12.2","11","14","5", "9")
KD <- c("5.6","8.6","12","8.6","9.4","6.2","9.2","6.4")
L <- c("20.2","13.2","9.2","11.8","11","21.2","17","12")
M <- c("5","13.2","12","12.6","12.8","9.6","3.6","9.6")
MP <- c("16","10","10.4","9.4","10.2","4.4","24.2","19.8")
S <- c("19.8","12.8","14.6","13","14.8","23.4","11.2","12.2")
SD <-c("10.8","16.8","15.6","13.8","10.4","10.6","14.6","6.4")
V <- c("9.4","13.4","15.8","18.6","20.4","10.6","15.2", "11")



df <- data.frame(Valkompasser, C, KD,L,M,MP,S,SD,V)
df
#----------------------------
dbDisconnect(con)

