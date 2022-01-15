from google.cloud import firestore
import datetime
class pool(object):
    def __init__(self):
        self.db = firestore.Client()
        self.time="14-16"
        self.date="2021-06-19"

        

    def delete_collection(self):
        coll=self.db.collections()
        for col in coll: 
            docs = col.limit(5).stream()
            deleted = 0

            for doc in docs:
                print(f'Deleting doc {doc.id} => {doc.to_dict()}')
                doc.reference.delete()
                deleted = deleted + 1
            if deleted >= 5:
                return delete_collection(col, 5)
    def get_state(self):
        coll=self.db.collections()
        lista=[]
        for col in coll:
            for doc in col.stream():
                diz=doc.to_dict()
                fascia=diz['time']
                fascia=fascia.split('-')
                fascia=int(fascia[0])
                ora=datetime.datetime.now().hour
                ora=ora+2
                data=datetime.datetime.today().strftime('%Y-%m-%d')
                dif=ora-fascia
                if dif==0 or dif==1 :
                    if diz['date']==data:    
                        lista.append(diz)
        return lista

    def get_res(self, user, date):
        try:
            ref = self.db.collection(f'{user}').document(f'{date}').get()
            if ref.exists:
                dic={}
                dic1={}
                dic=ref.to_dict()
                dic1['reservations']=dic
                return dic1
        except ValueError:
            return None
    def insert_res(self, user, date, **kwargs):
        return_val=[]
        ref = self.db.collection(f'{user}').document(f'{date}')
        coll=self.db.collections()
        cont=0
        for col in coll:
            for doc in col.stream():
                diz=doc.to_dict()
                if diz['date']==date and diz['time']==kwargs['time']:
                    cont=cont+1
        if cont==0 or cont==8:
            lane=4
        elif cont==1 or cont==9:
            lane=5
        elif cont==2 or cont==10:
            lane=3
        elif cont==3 or cont==11:
            lane=6
        elif cont==4 or cont==12:
            lane=2
        elif cont==5 or cont==13:
            lane=7
        elif cont==6 or cont==14:
            lane=1
        elif cont==7 or cont==15:
            lane=8 
        else:
            return "no available"
        ref.set({
            'date': date,
            'time': kwargs.get('time', self.time),
            'lane': lane
            })
        pisc={}
        pisc['date']=date
        pisc['time']=kwargs.get('time', self.time)
        pisc['lane']=lane
        return_val.append(pisc)
        if "others" in kwargs:
            lista1=[]
            for dict in kwargs['others']:
                date=dict['date']
                ref = self.db.collection(f'{user}').document(f'{date}')
                coll=self.db.collections()
                cont=0
                for col in coll:
                    for doc in col.stream():
                        diz=doc.to_dict()
                        if diz['date']==date and diz['time']==dict['time']:
                            cont=cont+1
                if cont==0 or cont==8:
                    lane=4
                elif cont==1 or cont==9:
                    lane=5
                elif cont==2 or cont==10:
                    lane=3
                elif cont==3 or cont==11:
                    lane=6
                elif cont==4 or cont==12:
                    lane=2
                elif cont==5 or cont==13:
                    lane=7
                elif cont==6 or cont==14:
                    lane=1
                elif cont==7 or cont==15:
                    lane=8 
                else:
                    return "no available"
                ref.set({
                    'date': dict['date'],
                    'time':dict['time'],
                    'lane':lane
                    })
                pisc={}
                pisc['date']=date
                pisc['time']=kwargs.get('time', self.time)
                pisc['lane']=lane
                return_val.append(pisc)
        ret_val={}
        ret_val['reservations']=return_val
        return ret_val

  


       


        


  