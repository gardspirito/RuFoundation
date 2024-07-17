from django.utils.http import urlsafe_base64_encode
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.core.mail import send_mail, BadHeaderError
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.shortcuts import redirect, resolve_url
from django.contrib.auth import get_user_model
from django.views.generic import FormView
from django.contrib.admin import site
from django.contrib import messages

from system.forms import InviteForm
from web.models.sites import get_current_site


User = get_user_model()


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return 'v2:' + str(user.pk) + str(timestamp) + str(user.is_active)


account_activation_token = TokenGenerator()


@method_decorator(staff_member_required, name='dispatch')
class InviteView(FormView):
    form_class = InviteForm
    template_name = "admin/system/user/invite.html"
    email_template_name = "mails/invite_email.txt"
    user = None

    def get_initial(self):
        initial = super(InviteView, self).get_initial()
        return initial

    def get_user(self) -> User | None:
        user_id = self.kwargs.get('id') or None
        if user_id:
            return User.objects.get(pk=user_id)
        return None

    def get_context_data(self, **kwargs):
        context = super(InviteView, self).get_context_data(**kwargs)
        context["title"] = "Пригласить пользователя"
        user = self.get_user()
        if user:
            context["title"] = "Активировать пользователя wd:%s" % user.wikidot_username
        context.update(site._wrapped.each_context(self.request))
        return context

    def get_success_url(self):
        return resolve_url("admin:index")

    def form_valid(self, form):
        email = form.cleaned_data['email']
        is_editor = form.cleaned_data['is_editor']
        user = self.get_user()
        if user:
            created = not user.email
        else:
            user, created = User.objects.get_or_create(email=email)
        site = get_current_site()
        if created:
            user.is_editor = is_editor
            user.is_active = False
            user.username = 'user-%d' % user.id
            user.email = email
            user.save()
            subject = f"Приглашение на {site.title}"
            c = {
                "email": user.email,
                'domain': self.request.get_host(),
                'site_name': site.title,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "user": user,
                'token': account_activation_token.make_token(user),
                'protocol': self.request.scheme,
            }
            content = render_to_string(self.email_template_name, c)
            try:
                send_mail(subject, content, None, [user.email], fail_silently=False)
                messages.success(self.request, "Приглашение успешно отправлено")
            except BadHeaderError:
                messages.error(self.request, "Неправильный заголовок")
        else:
            messages.error(self.request, "Данный email уже привязан к участнику сайта")

        return redirect(self.get_success_url())
