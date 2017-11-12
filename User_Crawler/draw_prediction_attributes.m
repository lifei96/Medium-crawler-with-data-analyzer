function draw_prediction_attributes()
    columns = {'Description', 'Likes', 'Followers', 'Followings', 'Lists', 'Tweets'};
    dataset = csvread('./data/prediction/dataset_1_train.csv', 1, 0);
    for k = 2:6
        figure(k-1);
        h1 = cdfplot(dataset(1:8000,k));
        set(h1, 'color', 'k', 'LineStyle', '--', 'LineWidth', 2);
        hold on;
        h2 = cdfplot(dataset(8001:16000,k));
        set(h2, 'color', 'k', 'LineStyle', '-', 'LineWidth', 2);
        if (k == 2)
            xlim([0 100000]);
            set(gca,'XScale','log');
        end
        if (k == 3)
            xlim([0 100000]);
            set(gca,'XScale','log');
        end
        if (k == 4)
            xlim([0 10000]);
            set(gca,'XScale','log');
        end
        if (k == 5)
            xlim([0 5000]);
            set(gca,'XScale','log');
        end
        if (k == 6)
            xlim([0 100000]);
            set(gca,'XScale','log');
        end
        set(gca, 'yticklabel', cellstr(num2str(get(gca,'ytick')'*100)));
        set(gca, 'FontSize', 12);
        xlabel(strjoin({'Number of', columns{k}}),'FontSize',20);
        ylabel('Percentage(%)','FontSize',20);
        legend('Less Influential', 'High Influential', 'Location', 'NorthWest');
        set(legend, 'FontSize', 20);
        title('');
        grid off;
        print(strjoin({'./results/prediction/attributes/CDF_prediction_', columns{k}, '.eps'}, ''), '-depsc');
    end
end