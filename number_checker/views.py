from django.shortcuts import render, redirect
from django.views import View
from .forms import PhoneCheckForm
from .logic import PhoneNumberManager
from .models import QueryHistory

class PhoneCheckView(View):
    template_name = 'number_checker/check_phone.html'
    
    def get(self, request):
        form = PhoneCheckForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = PhoneCheckForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {'form': form})
        
        phone_number = form.cleaned_data['phone_number']
        phone_obj = PhoneNumberManager.process_phone_number(phone_number, request)
        
        if not phone_obj:
            form.add_error('phone_number', 'Не удалось получить информацию о номере')
            return render(request, self.template_name, {'form': form})
        
        # Получаем историю запросов этого номера (исключая текущий)
        history = QueryHistory.objects.filter(
            phone_number=phone_obj
        ).order_by('-query_date')[:10]
        
        return render(request, 'number_checker/result.html', {
            'phone': phone_obj,
            'history': history
        })

class PhoneHistoryView(View):
    template_name = 'number_checker/history.html'
    
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
            
        history = QueryHistory.objects.filter(
            user=request.user
        ).select_related('phone_number').order_by('-query_date')[:50]
        
        return render(request, self.template_name, {'history': history})